// Practice widgets behind _includes/quiz.html and _includes/numeric.html.
//
// Multiple choice: .quiz[data-answer] with .choice[data-choice] buttons and an .explain block.
//   A wrong pick marks and disables that button; the right one marks it, disables all and
//   shows the explanation.
// Numeric: .numeric[data-answer][data-tol] with an .explain block. Checked within the absolute
//   tolerance. data-percent: the reader types a percentage, so "10.7" and "10.7%" both mean 0.107.
//   The input row and feedback line are built here.

(function () {
  const ICON = {
    check: '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    x: '<path d="M7 7l10 10M17 7L7 17"/>',
  };
  const icon = (name) => `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${ICON[name]}</svg>`;

  function setupChoice(box) {
    const answer = box.dataset.answer;
    const explain = box.querySelector(".explain");
    const buttons = box.querySelectorAll("button[data-choice]");
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const mark = button.querySelector(".mark");
        if (button.dataset.choice === answer) {
          button.classList.add("right");
          if (mark) mark.innerHTML = icon("check");
          buttons.forEach((b) => (b.disabled = true));
          if (explain) explain.classList.add("shown");
        } else {
          button.classList.add("wrong");
          if (mark) mark.innerHTML = icon("x");
          button.disabled = true;
        }
      });
    });
  }

  let count = 0;
  function setupNumeric(box) {
    const answer = parseFloat(box.dataset.answer);
    const tol = parseFloat(box.dataset.tol || "0");
    const percent = box.hasAttribute("data-percent");
    const explain = box.querySelector(".explain");
    const id = "numeric-" + ++count;

    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML =
      `<input class="field" id="${id}" type="text" inputmode="decimal" autocomplete="off" aria-label="Your answer">` +
      '<button class="btn btn-primary" type="button" data-check>Check</button>' +
      '<button class="btn btn-ghost" type="button" data-give-up>Show solution</button>';
    const input = row.querySelector("input");
    input.placeholder = percent ? "e.g. 12.3%" : "your answer";
    const feedback = document.createElement("p");
    feedback.className = "feedback";
    feedback.setAttribute("aria-live", "polite");
    box.insertBefore(row, explain);
    box.insertBefore(feedback, explain);

    function parse(text) {
      const clean = text.replace(",", ".").replace("%", "").replace("−", "-").trim();
      if (clean === "") return NaN;
      const value = parseFloat(clean);
      return percent ? value / 100 : value;
    }
    function say(kind, name, text) {
      feedback.className = "feedback " + kind;
      feedback.innerHTML = icon(name);
      feedback.append(text);
    }

    function grade() {
      if (input.readOnly) return;
      const value = parse(input.value);
      input.classList.remove("is-wrong", "is-right");
      if (Number.isNaN(value)) {
        input.classList.add("is-wrong");
        say("wrong", "x", "Type a number first.");
        return;
      }
      if (Math.abs(value - answer) <= tol + 1e-12) {
        input.classList.add("is-right");
        input.readOnly = true;
        say("right", "check", "Correct.");
        if (explain) explain.classList.add("shown");
      } else {
        input.classList.add("is-wrong");
        say("wrong", "x", `Not quite: ${value > answer ? "too high" : "too low"}. Try again.`);
      }
    }

    row.querySelector("[data-check]").addEventListener("click", grade);
    input.addEventListener("keydown", (event) => { if (event.key === "Enter") grade(); });
    row.querySelector("[data-give-up]").addEventListener("click", () => { if (explain) explain.classList.add("shown"); });
  }

  document.querySelectorAll(".quiz[data-answer]").forEach(setupChoice);
  document.querySelectorAll(".numeric[data-answer]").forEach(setupNumeric);
})();
