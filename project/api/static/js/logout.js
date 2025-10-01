document.getElementById("logoutBtn")?.addEventListener("click", async function () {
    const btn = this;
    const token = localStorage.getItem("token");

    const logoutUrl = btn.dataset.logoutUrl;
    const loginUrl = btn.dataset.loginUrl;
    const csrfToken = btn.dataset.csrfToken;

    if (!token) {
        window.location.href = loginUrl;
        return;
    }

    try {
        const response = await fetch(logoutUrl, {
            method: "POST",
            headers: {
                "Authorization": `Token ${token}`,
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            }
        });

        localStorage.removeItem("token");
        window.location.href = loginUrl;
    } catch (err) {
        console.error("Logout error:", err);
        localStorage.removeItem("token");
        window.location.href = loginUrl;
    }
});
