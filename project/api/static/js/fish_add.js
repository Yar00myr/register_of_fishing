document.addEventListener("DOMContentLoaded", function() {
    const formContainer = document.getElementById("catch-form-container");
    const addBtn = document.getElementById("add-catch");
    const totalForms = document.getElementById("id_form-TOTAL_FORMS");
    const emptyForm = document.getElementById("empty-form");

    if (!formContainer || !addBtn || !totalForms || !emptyForm) return;

    function updateTotalForms() {
        totalForms.value = formContainer.querySelectorAll(".catch-form").length;
    }

    function addForm() {
        const formCount = parseInt(totalForms.value);
        const newForm = emptyForm.cloneNode(true);
        newForm.classList.remove("d-none");
        newForm.classList.add("new-catch");
        newForm.innerHTML = newForm.innerHTML.replace(/__prefix__/g, formCount);
        formContainer.appendChild(newForm);
        updateTotalForms();
    }

    addBtn.addEventListener("click", function(e) {
        e.preventDefault();
        addForm();
    });

    formContainer.addEventListener("click", function(e) {
        if (e.target.classList.contains("remove-catch")) {
            e.preventDefault();

            const allForms = formContainer.querySelectorAll(".catch-form");
            const newForms = formContainer.querySelectorAll(".catch-form.new-catch");

            if (newForms.length > 0) {
                e.target.closest(".catch-form").remove();
                updateTotalForms();
            } else if (allForms.length > 1) {
                e.target.closest(".catch-form").remove();
                updateTotalForms();
            } 
        }
    });
});

