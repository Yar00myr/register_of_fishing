document.getElementById("loginForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const form = e.target;
    const email = form.email.value;
    const password = form.password.value;
    const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

    const loginUrl = form.dataset.loginUrl;

    const response = await fetch(loginUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    const errorDiv = document.getElementById("error");

    if (response.ok) {
        localStorage.setItem("token", data.token);
        window.location.href = "/";
    } else {
        let message = "Login failed";
        if (data.errors) {
            if (data.errors.non_field_errors) {
                message = data.errors.non_field_errors.join(", ");
            } else {

                const firstKey = Object.keys(data.errors)[0];
                message = data.errors[firstKey].join(", ");
            }
        }
        errorDiv.innerHTML = `<i class="bi bi-exclamation-circle"></i> ${message}`;
        errorDiv.classList.remove("d-none");
    }

});