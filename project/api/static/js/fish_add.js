const form = document.getElementById("fishTypeForm");

if (form) {
    const url = form.getAttribute("data-url");
    const message = document.getElementById("fishMessage");
    const list = document.getElementById("fishList");

    form.addEventListener("submit", async function(e) {
        e.preventDefault();

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const formData = new FormData(form);

        const response = await fetch(url, {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken },
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            message.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            list.innerHTML += `<li class="list-group-item d-flex justify-content-between align-items-center">🐟 ${data.name}</li>`;
            form.reset();
        } else {
            const errors = Object.values(data.errors).flat().join("<br>");
            message.innerHTML = `<div class="alert alert-danger">${errors}</div>`;
        }
    });
}
