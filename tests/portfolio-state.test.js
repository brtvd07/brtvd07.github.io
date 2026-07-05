"use strict";

const test = require("node:test");
const assert = require("node:assert/strict");
const { createPortfolioController, createMenuController, validateCatalog } = require("../assets/js/portfolio-state.js");

const valid = require("../assets/data/projects.json");

test("loading preserves filter and resolve renders active filter", async () => {
  let resolve;
  const rendered = [];
  const disabled = [];
  const phases = [];
  const controller = createPortfolioController({
    loadCatalog: () => new Promise((done) => { resolve = done; }),
    render: (items) => rendered.push(items),
    renderError: () => assert.fail("unexpected error"),
    renderLoading: () => phases.push("loading"),
    setFiltersDisabled: (value) => disabled.push(value),
  });
  const pending = controller.load();
  controller.setFilter("python");
  assert.equal(controller.state.phase, "loading");
  assert.equal(controller.state.activeFilter, "python");
  assert.equal(rendered.length, 0);
  resolve(valid);
  await pending;
  assert.equal(controller.state.phase, "ready");
  assert.deepEqual(phases, ["loading"]);
  assert.ok(rendered.at(-1).every((project) => project.kind === "python"));
  assert.deepEqual(disabled, [true, false]);
});

test("failure survives filter clicks and retry recovers", async () => {
  let attempts = 0;
  let retry;
  const rendered = [];
  const phases = [];
  const controller = createPortfolioController({
    loadCatalog: async () => { if (attempts++ === 0) throw new Error("offline"); return valid; },
    render: (items) => rendered.push(items),
    renderError: (_error, action) => { retry = action; },
    renderLoading: () => phases.push("loading"),
    setFiltersDisabled: () => {},
  });
  await controller.load();
  assert.equal(controller.state.phase, "error");
  controller.setFilter("web");
  assert.equal(controller.state.phase, "error");
  assert.equal(rendered.length, 0);
  await retry();
  assert.equal(controller.state.phase, "ready");
  assert.deepEqual(phases, ["loading", "loading"]);
  assert.ok(rendered.at(-1).every((project) => project.kind === "web"));
});

test("catalog validation rejects unsafe runtime URLs", () => {
  const unsafe = structuredClone(valid);
  unsafe[0].demo_url = "javascript:alert(1)";
  assert.throws(() => validateCatalog(unsafe), /demo_url/);
  unsafe[0].demo_url = "https://evil.example@brtvd07.github.io/demo";
  assert.throws(() => validateCatalog(unsafe), /demo_url/);
});

test("menu labels state and Escape restores toggle focus", () => {
  const handlers = {};
  const toggle = fakeElement(handlers);
  const nav = fakeElement();
  const document = { addEventListener: (type, fn) => { handlers[type] = fn; } };
  createMenuController({ toggle, nav, document });
  handlers.click();
  assert.equal(toggle.attrs["aria-label"], "Закрыть меню");
  handlers.keydown({ key: "Escape" });
  assert.equal(toggle.attrs["aria-label"], "Открыть меню");
  assert.equal(toggle.focused, true);
});

function fakeElement(handlers = {}) {
  return {
    attrs: { "aria-expanded": "false" }, focused: false,
    classList: { toggle() {}, remove() {} },
    addEventListener(type, fn) { handlers[type] = fn; },
    getAttribute(name) { return this.attrs[name]; },
    setAttribute(name, value) { this.attrs[name] = value; },
    focus() { this.focused = true; },
  };
}
