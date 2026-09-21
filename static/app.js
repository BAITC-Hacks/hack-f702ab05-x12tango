const chat = document.getElementById("chat");
const form = document.getElementById("composer");
const input = document.getElementById("input");
const suggestions = document.getElementById("suggestions");

function addMessage(text, role, { unknown = false } = {}) {
  const el = document.createElement("div");
  el.className = `msg msg--${role}${unknown ? " msg--unknown" : ""}`;
  el.textContent = text;
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
  return el;
}

function showTyping() {
  const el = document.createElement("div");
  el.className = "typing";
  el.id = "typing";
  el.innerHTML = "<span></span><span></span><span></span>";
  chat.appendChild(el);
  chat.scrollTop = chat.scrollHeight;
}

function hideTyping() {
  const el = document.getElementById("typing");
  if (el) el.remove();
}

async function ask(question) {
  addMessage(question, "user");
  showTyping();

  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });
    const data = await res.json();

    await new Promise((r) => setTimeout(r, 350 + Math.random() * 250));
    hideTyping();
    addMessage(data.answer, "bot", { unknown: !data.matched });
  } catch (err) {
    hideTyping();
    addMessage("Ошибка соединения с сервером.", "bot", { unknown: true });
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const question = input.value.trim();
  if (!question) return;
  input.value = "";
  ask(question);
});

suggestions.addEventListener("click", (e) => {
  const chip = e.target.closest(".chip");
  if (!chip) return;
  ask(chip.dataset.question);
});

addMessage(
  "Привет! Я отвечаю на вопросы про репетицию хакатона: время, команда, трек, сдача, призы. Спросите или выберите готовый вопрос ниже 👇",
  "bot"
);
