(() => {
  function initFormset(root) {
    const container = root.querySelector("[data-formset-container]");
    const template = root.querySelector("template[data-formset-template]");
    const addButton = root.querySelector("[data-formset-add]");
    const totalForms = root.querySelector("input[name$='-TOTAL_FORMS']");
    if (!container || !template || !addButton || !totalForms) return;

    addButton.addEventListener("click", () => {
      const index = Number(totalForms.value);
      container.insertAdjacentHTML(
        "beforeend",
        template.innerHTML.replaceAll("__prefix__", index)
      );
      totalForms.value = index + 1;
    });

    container.addEventListener("click", (e) => {
      const removeButton = e.target.closest("[data-formset-remove]");
      if (!removeButton) return;

      const row = removeButton.closest("[data-formset-row]");
      if (row.dataset.existing === "1") {
        const deleteInput = row.querySelector("input[name$='-DELETE']");
        if (deleteInput) deleteInput.checked = true;
        row.classList.add("d-none");
      } else {
        row.remove();
      }
    });
  }

  document.querySelectorAll("[data-formset]").forEach(initFormset);
})();