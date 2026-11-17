// Practice widgets shared by every lesson. Include with:
//   <script src="../assets/quiz.js" defer></script>
//
// Multiple choice:
//   <div class="quiz" data-answer="b">
//     <p class="q">Question?</p>
//     <div class="choices">
//       <button data-choice="a">...</button>
//       <button data-choice="b">...</button>
//     </div>
//     <p class="explain">Why the right answer is right.</p>
//   </div>
//
// Numeric answer, checked within a tolerance (absolute):
//   <div class="numeric" data-answer="0.9975" data-tol="0.0002">
//     <p class="q">Compute ...</p>
//     <p class="explain">Worked solution, shown once answered correctly or given up.</p>
//   </div>
// Percent answers: add data-percent, so "10.7" and "10.7%" both mean 0.107.

(function () {
  function setupChoice(box) {
    const answer = box.dataset.answer;
    const explain = box.querySelector(".explain");
    const buttons = box.querySelectorAll("button[data-choice]");
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        if (button.dataset.choice === answer) {
          button.classList.add("right");
          buttons.forEach((b) => (b.disabled = true));
          if (explain) explain.classList.add("shown");
        } else {
          button.classList.add("wrong");
          button.disabled = true;
        }
      });
    });
  }

  function setupNumeric(box) {
    const answer = parseFloat(box.dataset.answer);
    const tol = parseFloat(box.dataset.tol || "0");
    const percent = box.hasAttribute("data-percent");
    const explain = box.querySelector(".explain");

    const row = document.createElement("div");
    row.className = "row";
    const input = document.createElement("input");
    input.type = "text";
    input.inputMode = "decimal";
    input.placeholder = percent ? "e.g. 12.3%" : "your answer";
    const check = document.createElement("button");
    check.textContent = "Check";
    const giveUp = document.createElement("button");
    giveUp.textContent = "Show solution";
    row.append(input, check, giveUp);
    const feedback = document.createElement("p");
    feedback.className = "feedback";
    box.insertBefore(row, explain);
    box.insertBefore(feedback, explain);

    function parse(text) {
      const clean = text.replace(",", ".").replace("%", "").trim();
      if (clean === "") return NaN;
      const value = parseFloat(clean);
      return percent ? value / 100 : value;
    }

    function grade() {
      const value = parse(input.value);
      if (Number.isNaN(value)) {
        feedback.textContent = "Type a number first.";
        feedback.className = "feedback wrong";
        return;
      }
      if (Math.abs(value - answer) <= tol) {
        feedback.textContent = "Correct.";
        feedback.className = "feedback right";
        if (explain) explain.classList.add("shown");
      } else {
        const direction = value > answer ? "too high" : "too low";
        feedback.textContent = `Not quite: ${direction}. Try again.`;
        feedback.className = "feedback wrong";
      }
    }

    check.addEventListener("click", grade);
    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter") grade();
    });
    giveUp.addEventListener("click", () => {
      if (explain) explain.classList.add("shown");
    });
  }

  document.querySelectorAll(".quiz").forEach(setupChoice);
  document.querySelectorAll(".numeric").forEach(setupNumeric);
})();
