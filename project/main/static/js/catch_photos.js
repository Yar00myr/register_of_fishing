(() => {
  const container = document.querySelector("[data-formset-container]");
  if (!container) return;

  container.addEventListener("click", (e) => {
    const replaceBtn = e.target.closest(".btn-replace-photo");
    if (!replaceBtn) return;
    replaceBtn.classList.add("d-none");
    replaceBtn
      .closest(".replace-photo-wrap")
      .querySelector(".replace-input")
      .classList.remove("d-none");
  });

  container.addEventListener("change", (e) => {
    const checkbox = e.target.closest("input[type='checkbox'][name$='-DELETE']");
    if (checkbox) {
      checkbox.closest("[data-formset-row]").classList.toggle("marked-delete", checkbox.checked);
    }
  });
})();