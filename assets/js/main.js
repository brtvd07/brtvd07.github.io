"use strict";

const grid = document.querySelector("#project-grid");
const filterButtons = [...document.querySelectorAll("[data-filter]")];
const { createPortfolioController, createMenuController, validateProject } = globalThis.PortfolioState;

function projectCard(rawProject, index) {
  const project = validateProject(rawProject);
  const article = document.createElement("article");
  article.className = "project-card";
  article.dataset.kind = project.kind;
  const meta = document.createElement("div");
  meta.className = "project-meta";
  const number = document.createElement("span");
  number.className = "project-index";
  number.textContent = String(index + 1).padStart(2, "0");
  const kind = document.createElement("span");
  kind.textContent = project.kind === "web" ? "Web" : "Python";
  meta.append(number, kind);
  if (project.demo) {
    const demo = document.createElement("span");
    demo.className = "demo-label";
    demo.textContent = "Демо-проект";
    meta.append(demo);
  }
  const title = document.createElement("h3");
  title.textContent = project.name;
  const summary = document.createElement("p");
  summary.textContent = project.summary;
  const proof = document.createElement("p");
  proof.className = "project-proof";
  proof.textContent = project.proof;
  const links = document.createElement("div");
  links.className = "project-links";
  const repository = document.createElement("a");
  repository.href = project.repo_url;
  repository.textContent = "GitHub →";
  const demonstration = document.createElement("a");
  demonstration.href = project.demo_url;
  demonstration.textContent = project.kind === "web" ? "Открыть демо →" : "Сценарий запуска →";
  links.append(repository, demonstration);
  article.append(meta, title, summary, proof, links);
  return article;
}

function render(projects) {
  grid.dataset.phase = "ready";
  grid.setAttribute("aria-busy", "false");
  grid.replaceChildren(...projects.map(projectCard));
}

function renderError(_error, retry) {
  grid.dataset.phase = "error";
  grid.setAttribute("aria-busy", "false");
  const message = document.createElement("p");
  message.className = "error";
  message.textContent = "Не удалось загрузить каталог. ";
  const button = document.createElement("button");
  button.type = "button";
  button.textContent = "Повторить";
  button.addEventListener("click", retry);
  message.append(button);
  grid.replaceChildren(message);
}

function renderLoading() {
  grid.dataset.phase = "loading";
  grid.setAttribute("aria-busy", "true");
  const message = document.createElement("p");
  message.className = "loading";
  message.textContent = "Загружаю проекты…";
  grid.replaceChildren(message);
}

function setFiltersDisabled(disabled) {
  filterButtons.forEach((button) => { button.disabled = disabled; });
}

const controller = createPortfolioController({
  loadCatalog: async () => {
    const response = await fetch("assets/data/projects.json");
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
  },
  render,
  renderError,
  renderLoading,
  setFiltersDisabled,
});

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle("active", active);
      item.setAttribute("aria-pressed", String(active));
    });
    controller.setFilter(button.dataset.filter);
  });
});

createMenuController({
  toggle: document.querySelector(".nav-toggle"),
  nav: document.querySelector("#site-nav"),
  document,
});
document.querySelector("#year").textContent = String(new Date().getFullYear());
controller.load();
