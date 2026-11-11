(() => {
  const KEY = "fishing-theme";
  const html = document.documentElement;
  const btn = document.getElementById("themeToggle");
  const icon = document.getElementById("themeIcon");
  if (!btn || !icon) return;

  const read = () => {
    try { return localStorage.getItem(KEY); } catch { return null; }
  };
  const write = (value) => {
    try { localStorage.setItem(KEY, value); } catch { /* storage unavailable */ }
  };

  function applyTheme(theme) {
    html.setAttribute("data-theme", theme);
    icon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-fill";
    btn.title = theme === "dark" ? "Switch to light mode" : "Switch to dark mode";
  }

  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  applyTheme(read() || (prefersDark ? "dark" : "light"));

  btn.addEventListener("click", () => {
    const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next);
    write(next);
  });
})();