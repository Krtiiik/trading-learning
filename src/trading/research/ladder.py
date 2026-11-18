"""The claim ladder: where each hypothesis stands, computed from its file and its run records.

    registered      prediction, test and decision rule committed first
    tested (train)  -> rejected          kept as a negative result
    candidate       passes Benjamini-Hochberg at 10% across the primary train test of ALL
                    registered literature hypotheses (untested ones count with p = 1)
    replicated(dev) -> not replicated    kept, flagged
    supported       same sign, at least the pre-declared size on dev
    skeptic review  -> refuted           kept, with the reason
    confirmed       eligible as a test-set finalist

A hypothesis that came from exploring train data cannot be tested on train: its dev result is
the evidence, and the dev p-values of all exploration hypotheses pass through their own
Benjamini-Hochberg control. Nobody sets a status by hand; it follows from the records.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from trading.research.registry import Hypothesis
from trading.research.runs import latest
from trading.stats import benjamini_hochberg

FDR = 0.10
"""False-discovery rate for both controls: train tests of literature hypotheses, and dev tests
of exploration hypotheses."""

DEFAULT_MIN_RATIO = 0.5
"""Proposed default for "meaningful size": the dev estimate is at least half the train one."""

REGISTERED = "registered"
REJECTED = "rejected"
CANDIDATE = "candidate"
NOT_REPLICATED = "not replicated"
SUPPORTED = "supported"
REFUTED = "refuted"
CONFIRMED = "confirmed"

AT_LEAST_CANDIDATE = (CANDIDATE, NOT_REPLICATED, SUPPORTED, REFUTED, CONFIRMED)


@dataclass
class Standing:
    hypothesis: Hypothesis
    status: str = REGISTERED
    train: dict[str, Any] | None = None
    dev: dict[str, Any] | None = None
    test: dict[str, Any] | None = None
    q_value: float | None = None
    """Benjamini-Hochberg adjusted p-value: of the train test (literature) or dev test (exploration)."""
    reasons: list[str] = field(default_factory=list)


def standings(hypotheses: list[Hypothesis], runs: list[dict[str, Any]]) -> dict[str, Standing]:
    """The ladder status of every hypothesis, given all run records."""
    table = {
        hypothesis.id: Standing(
            hypothesis,
            train=latest(runs, hypothesis, "train"),
            dev=latest(runs, hypothesis, "dev"),
            test=latest(runs, hypothesis, "test"),
        )
        for hypothesis in hypotheses
    }
    _control(table, "literature", "train")
    _control(table, "exploration", "dev")
    for standing in table.values():
        _place(standing)
    return table


def _control(table: dict[str, Standing], origin: str, segment: str) -> None:
    """False-discovery control across every hypothesis of one origin; untested ones count as p = 1."""
    family = [standing for standing in table.values() if standing.hypothesis.origin == origin]
    p_values = [
        run["p_value"] if (run := getattr(standing, segment)) is not None else 1.0
        for standing in family
    ]
    _, adjusted = benjamini_hochberg(p_values, FDR)
    for standing, q_value in zip(family, adjusted):
        if getattr(standing, segment) is not None:
            standing.q_value = float(q_value)


def _place(standing: Standing) -> None:
    hypothesis, reasons = standing.hypothesis, standing.reasons
    sign = 1.0 if hypothesis.direction == "positive" else -1.0
    rule = hypothesis.dev_rule
    minimum = float(rule["min_size"])

    if hypothesis.origin == "literature":
        if standing.train is None:
            return
        passed = standing.q_value is not None and standing.q_value <= FDR
        reasons.append(
            f"train p = {standing.train['p_value']:.4f}, q = {standing.q_value:.4f} "
            f"({'passes' if passed else 'fails'} false-discovery control at {FDR:.0%})"
        )
        if not passed:
            standing.status = REJECTED
            return
        standing.status = CANDIDATE
        if standing.dev is None:
            return
        train_size = sign * standing.train["estimate"]
        dev_size = sign * standing.dev["estimate"]
        needed = max(float(rule.get("min_ratio", DEFAULT_MIN_RATIO)) * train_size, minimum)
        replicated = dev_size >= needed
        reasons.append(
            f"dev estimate {standing.dev['estimate']:+.4f} against a required "
            f"{sign * needed:+.4f} (train {standing.train['estimate']:+.4f})"
        )
    else:
        if standing.dev is None:
            return
        passed = standing.q_value is not None and standing.q_value <= FDR
        dev_size = sign * standing.dev["estimate"]
        replicated = passed and dev_size >= minimum
        reasons.append(
            f"dev p = {standing.dev['p_value']:.4f}, q = {standing.q_value:.4f} across exploration "
            f"hypotheses; estimate {standing.dev['estimate']:+.4f} against a required {sign * minimum:+.4f}"
        )
    if not replicated:
        standing.status = NOT_REPLICATED
        return
    standing.status = SUPPORTED
    verdict = (hypothesis.skeptic or {}).get("verdict")
    if verdict in (CONFIRMED, REFUTED):
        standing.status = verdict
        reasons.append(f"Skeptic: {verdict}")


def load_standings(records: Path) -> dict[str, Standing]:
    from trading.research.registry import load_all
    from trading.research.runs import load_runs

    return standings(load_all(records), load_runs(records))
