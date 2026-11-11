(() => {
  const collapse = document.getElementById("fishSectionCollapse");
  const chevron = document.getElementById("fishChevron");
  if (!collapse || !chevron) return;

  collapse.addEventListener("show.bs.collapse", () => chevron.classList.add("rotated"));
  collapse.addEventListener("hide.bs.collapse", () => chevron.classList.remove("rotated"));
})();