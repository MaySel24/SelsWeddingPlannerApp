document.addEventListener("DOMContentLoaded", () => {
    const darkModeKey = "dark-mode";
    const body = document.body;
    const darkModeToggle = document.getElementById("darkModeToggle");

    // Function to toggle dark mode
    function applyDarkMode(enabled) {
        body.classList.toggle("dark-mode", enabled);
        document.querySelectorAll(".card, .table, .modal-content")?.forEach(el =>
            el.classList.toggle("dark-mode-element", enabled)
        );

        // Ensure icons and SVGs also change
        document.querySelectorAll(".icon, i, svg")?.forEach(icon => {
            icon.style.color = enabled ? "white" : ""; // Inherit default color
            icon.style.fill = enabled ? "white" : "";
        });

        // Save preference
        localStorage.setItem(darkModeKey, enabled ? "enabled" : "disabled");
    }

    // Apply saved dark mode preference
    const isDarkMode = localStorage.getItem(darkModeKey) === "enabled";
    applyDarkMode(isDarkMode);

    // Toggle dark mode on button click
    darkModeToggle?.addEventListener("click", () => {
        applyDarkMode(!body.classList.contains("dark-mode"));
    });

    // Delete Confirmation
    document.querySelectorAll(".delete-btn")?.forEach(button =>
        button.addEventListener("click", event => {
            if (!confirm("Are you sure you want to delete this?")) {
                event.preventDefault();
            }
        })
    );
});