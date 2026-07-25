"use strict";

(function expose(root) {
  const ids = ["skillary", "glowstudio", "nordmarket", "stroyraschet", "flowdesk", "telegram-freelance-agent", "telegram-expense-bot", "ai-support-bot", "booking-crm-bot"];
  const fields = ["id", "name", "kind", "summary", "repo_url", "demo_url", "proof", "demo"];
  const demoPaths = new Set([
    "../skillary/", "../glowstudio/", "../nordmarket/", "../stroyraschet/", "../flowdesk/",
    "../telegram-freelance-agent/README.md", "../telegram-expense-bot/README.md",
    "../ai-support-bot/demo/", "../booking-crm-bot/demo/",
  ]);

  function validateProject(project) {
    if (!project || Object.keys(project).sort().join() !== [...fields].sort().join()) throw new Error("invalid project fields");
    if (!ids.includes(project.id)) throw new Error("invalid id");
    if (!['web', 'python'].includes(project.kind)) throw new Error("invalid kind");
    if (![project.name, project.summary, project.proof].every((value) => typeof value === "string" && value.trim())) throw new Error("invalid project text");
    if (typeof project.demo !== "boolean") throw new Error("invalid demo flag");
    const repo = new URL(project.repo_url);
    if (repo.protocol !== "https:" || repo.hostname !== "github.com" || repo.pathname !== `/brtvd07/${project.id}` || repo.username || repo.password || repo.port || repo.search || repo.hash) throw new Error("invalid repo_url");
    if (!demoPaths.has(project.demo_url)) {
      const demo = new URL(project.demo_url);
      const allowedDemoHost =
        demo.hostname === "brtvd07.github.io" ||
        (demo.hostname === "github.com" && demo.pathname.startsWith("/brtvd07/"));
      if (demo.protocol !== "https:" || !allowedDemoHost || demo.username || demo.password || demo.port) throw new Error("invalid demo_url");
    }
    return project;
  }

  function validateCatalog(catalog) {
    if (!Array.isArray(catalog) || catalog.length !== 9) throw new Error("catalog must contain 9 projects");
    catalog.forEach(validateProject);
    if (new Set(catalog.map((item) => item.id)).size !== 9) throw new Error("duplicate id");
    if (new Set(catalog.map((item) => item.name)).size !== 9) throw new Error("duplicate name");
    return catalog;
  }

  function createPortfolioController(dependencies) {
    const state = { phase: "loading", activeFilter: "all", catalog: [] };
    const visible = () => state.catalog.filter((item) => state.activeFilter === "all" || item.kind === state.activeFilter);
    async function load() {
      state.phase = "loading";
      dependencies.renderLoading();
      dependencies.setFiltersDisabled(true);
      try {
        state.catalog = validateCatalog(await dependencies.loadCatalog());
        state.phase = "ready";
        dependencies.setFiltersDisabled(false);
        dependencies.render(visible());
      } catch (error) {
        state.phase = "error";
        dependencies.setFiltersDisabled(true);
        dependencies.renderError(error, load);
      }
    }
    function setFilter(filter) {
      if (!["all", "web", "python"].includes(filter)) return;
      state.activeFilter = filter;
      if (state.phase === "ready") dependencies.render(visible());
    }
    return { state, load, setFilter };
  }

  function createMenuController({ toggle, nav, document }) {
    function close(restoreFocus = false) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Открыть меню");
      nav.classList.remove("open");
      if (restoreFocus) toggle.focus();
    }
    toggle.setAttribute("aria-label", "Открыть меню");
    toggle.addEventListener("click", () => {
      const opening = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(opening));
      toggle.setAttribute("aria-label", opening ? "Закрыть меню" : "Открыть меню");
      nav.classList.toggle("open", opening);
    });
    document.addEventListener("keydown", (event) => { if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") close(true); });
    nav.addEventListener("click", (event) => { if (event.target && event.target.closest && event.target.closest("a")) close(); });
    return { close };
  }

  const api = { createPortfolioController, createMenuController, validateCatalog, validateProject };
  root.PortfolioState = api;
  if (typeof module !== "undefined") module.exports = api;
})(globalThis);
