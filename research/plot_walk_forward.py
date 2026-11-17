"""Equity and drawdown of SPY, 60/40 and the capped 60/40 on the walk-forward window.

Writes research/figures/walk_forward.png. Reads sealed data only.

Run: uv run python research/plot_walk_forward.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

from common import evaluate, research_market, research_prices
from trading.strategies import rules

SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
COLORS = {"SPY buy & hold": "#2a78d6", "60/40 SPY/IEF": "#eb6834", "Capped 60/40": "#1baf7a"}

market = research_market()
prices = research_prices()
mix = rules.fixed_mix(prices, {"SPY": 0.6, "IEF": 0.4})
results = {
    "SPY buy & hold": evaluate(market, rules.fixed_mix(prices, {"SPY": 1.0})),
    "60/40 SPY/IEF": evaluate(market, mix),
    "Capped 60/40": evaluate(market, rules.volatility_cap(mix, prices, 0.08, 20), rebalance_band=0.05),
}

figure, (top, bottom) = plt.subplots(
    2, 1, figsize=(10, 7), sharex=True, height_ratios=[3, 2], facecolor=SURFACE
)
for axis in (top, bottom):
    axis.set_facecolor(SURFACE)
    axis.grid(True, axis="y", color=GRID, linewidth=0.8)
    axis.tick_params(colors=MUTED, length=0, labelsize=9)
    for side in ("top", "right", "left"):
        axis.spines[side].set_visible(False)
    axis.spines["bottom"].set_color(GRID)

for name, result in results.items():
    equity = result.equity
    top.plot(equity.index, equity, color=COLORS[name], linewidth=2, label=name)
    top.annotate(f"{name}  ${equity.iloc[-1]:,.0f}", (equity.index[-1], equity.iloc[-1]),
                 xytext=(6, 0), textcoords="offset points", va="center", fontsize=9, color=INK)
    drawdown = equity / equity.cummax() - 1
    bottom.plot(drawdown.index, drawdown, color=COLORS[name], linewidth=1.5, label=name)

top.set_yscale("log")
top.set_yticks([5_000, 10_000, 20_000, 40_000, 80_000])
top.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}"))
top.minorticks_off()
top.set_title("$10,000 from 2005-01-03 to 2024-11-15, after 5 bps per side (log scale)",
              loc="left", fontsize=11, color=INK)
top.legend(frameon=False, fontsize=9, labelcolor=INK, loc="upper left")
bottom.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
bottom.set_title("Drawdown from the previous peak", loc="left", fontsize=11, color=INK)
figure.subplots_adjust(right=0.78, hspace=0.18)

out = Path(__file__).parent / "figures"
out.mkdir(exist_ok=True)
figure.savefig(out / "walk_forward.png", dpi=130, facecolor=SURFACE)
print(out / "walk_forward.png")
