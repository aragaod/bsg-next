// Mobile menu toggle
const toggle = document.querySelector("[data-menu-toggle]");
const menu = document.getElementById("mobile-menu");
if (toggle && menu) {
  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!open));
    menu.classList.toggle("hidden", open);
  });
}

// Technique filters (Resources, Training). Items without data-tech values
// are general and stay visible under every filter.
document.querySelectorAll("[data-filter]").forEach((bar) => {
  const scope = document.querySelector(bar.dataset.filter);
  if (!scope) return;
  bar.hidden = false;
  const buttons = bar.querySelectorAll("button[data-value]");
  const apply = (value) => {
    buttons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.value === value)));
    scope.querySelectorAll("[data-tech]").forEach((item) => {
      const techs = item.dataset.tech.split(" ").filter(Boolean);
      item.hidden = value !== "all" && techs.length > 0 && !techs.includes(value);
    });
    scope.querySelectorAll("[data-filter-group]").forEach((group) => {
      group.hidden = !group.querySelector("[data-tech]:not([hidden])");
    });
  };
  buttons.forEach((b) => b.addEventListener("click", () => apply(b.dataset.value)));
});

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Announcement bar: rotate messages every 7 s; pause on hover/focus.
document.querySelectorAll("[data-rotator]").forEach((bar) => {
  const items = [...bar.querySelectorAll("[data-rotator-item]")];
  if (items.length < 2) return;
  let i = 0;
  let paused = false;
  const show = (n) => {
    items[i].classList.add("hidden");
    items[i].setAttribute("aria-hidden", "true");
    i = (n + items.length) % items.length;
    items[i].classList.remove("hidden");
    items[i].removeAttribute("aria-hidden");
  };
  bar.querySelector("[data-rotator-prev]")?.addEventListener("click", () => show(i - 1));
  bar.querySelector("[data-rotator-next]")?.addEventListener("click", () => show(i + 1));
  ["mouseenter", "focusin"].forEach((e) => bar.addEventListener(e, () => (paused = true)));
  ["mouseleave", "focusout"].forEach((e) => bar.addEventListener(e, () => (paused = false)));
  if (!reduceMotion) setInterval(() => !paused && show(i + 1), 7000);
});

// Meeting countdown: days / hours / minutes until the start date (UK time is
// close enough for a day-level countdown); "Happening now" until the end date.
document.querySelectorAll("[data-countdown]").forEach((box) => {
  const start = new Date(box.dataset.countdown + "T09:00:00");
  const end = new Date((box.dataset.countdownEnd || box.dataset.countdown) + "T18:00:00");
  const units = Object.fromEntries([...box.querySelectorAll("[data-unit]")].map((el) => [el.dataset.unit, el]));
  const now = box.querySelector("[data-countdown-now]");
  const tick = () => {
    const t = Date.now();
    if (t >= start && t <= end) {
      Object.values(units).forEach((el) => (el.parentElement.hidden = true));
      now.hidden = false;
      return;
    }
    const ms = Math.max(0, start - t);
    units.days.textContent = Math.floor(ms / 864e5);
    units.hours.textContent = Math.floor((ms % 864e5) / 36e5);
    units.minutes.textContent = Math.floor((ms % 36e5) / 6e4);
  };
  tick();
  setInterval(tick, 30000);
});

// Carousel arrows: scroll the track by roughly one screen of cards.
document.querySelectorAll("[data-carousel]").forEach((c) => {
  const track = c.querySelector("[data-carousel-track]");
  const step = () => track.clientWidth * 0.9;
  const behavior = reduceMotion ? "auto" : "smooth";
  c.querySelector("[data-carousel-prev]")?.addEventListener("click", () => track.scrollBy({ left: -step(), behavior }));
  c.querySelector("[data-carousel-next]")?.addEventListener("click", () => track.scrollBy({ left: step(), behavior }));
});

// Mol* 3D viewer, loaded on request.
const loadOnce = (() => {
  let p;
  return (js, css) =>
    (p ??= new Promise((resolve, reject) => {
      const l = document.createElement("link");
      l.rel = "stylesheet";
      l.href = css;
      document.head.append(l);
      const s = document.createElement("script");
      s.src = js;
      s.onload = resolve;
      s.onerror = reject;
      document.head.append(s);
    }));
})();
document.querySelectorAll("[data-molstar]").forEach((box) => {
  box.querySelector("[data-molstar-load]")?.addEventListener("click", async (ev) => {
    const btn = ev.currentTarget;
    btn.querySelector("span").textContent = "Loading…";
    try {
      await loadOnce(box.dataset.molstarJs, box.dataset.molstarCss);
      const host = document.createElement("div");
      host.style.cssText = "position:absolute;inset:0";
      box.append(host);
      const viewer = await window.molstar.Viewer.create(host, {
        layoutIsExpanded: false,
        layoutShowControls: false,
        layoutShowRemoteState: false,
        layoutShowSequence: false,
        layoutShowLog: false,
        layoutShowLeftPanel: false,
        viewportShowExpand: true,
        viewportShowSelectionMode: false,
        viewportShowAnimation: false,
        pdbProvider: "pdbe",
      });
      await viewer.loadPdb(box.dataset.molstar);
      btn.remove();
    } catch (e) {
      btn.querySelector("span").textContent = "Could not load the viewer. Please try again.";
    }
  });
});
