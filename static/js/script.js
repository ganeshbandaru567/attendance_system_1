document.addEventListener("DOMContentLoaded", function () {
        const sendBtn = document.querySelector(".conrow-2 button");

        if (sendBtn) {
            sendBtn.addEventListener("click", function () {
                const name = document.querySelector(".search").value;
                const email = document.querySelectorAll(".search-input")[1].value;
                const subject = document.querySelectorAll(".search-input")[2].value;
                const message = document.querySelector(".ser-msg").value;

                if (!name || !email || !subject || !message) {
                    alert("Please fill in all fields before submitting.");
                } else {
                    alert("Thank you, " + name + "! Your message has been sent.");
                }
            });
        }
    });
    document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.querySelector("#password");
    const showPasswordCheckbox = document.querySelector("#showPassword");

    if (passwordInput && showPasswordCheckbox) {
        showPasswordCheckbox.addEventListener("change", function () {
            passwordInput.type = this.checked ? "text" : "password";
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const messageBox = document.querySelector(".ser-msg");
    const charCounter = document.getElementById("charCount");

    if (messageBox && charCounter) {
        messageBox.addEventListener("input", function () {
            charCounter.textContent = `${messageBox.value.length} / 300`;
        });
    }
});





document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".nav-links ul li a");
    const currentPath = window.location.pathname.replace(/\/+$/, '') || '/';

    links.forEach(link => {
        const linkPath = new URL(link.href).pathname.replace(/\/+$/, '');
        if (linkPath === currentPath) {
            link.classList.add("active-link");
        }
    });
});




document.addEventListener("DOMContentLoaded", function () {
    const usernameInput = document.getElementById("username");
    if (usernameInput) {
        usernameInput.focus();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password");
    const strengthDisplay = document.getElementById("password-strength");

    if (passwordInput && strengthDisplay) {
        passwordInput.addEventListener("input", function () {
            const val = passwordInput.value;
            let strength = "Weak";

            if (val.length >= 8 && /[A-Z]/.test(val) && /\d/.test(val)) {
                strength = "Strong";
            } else if (val.length >= 6) {
                strength = "Moderate";
            }

            strengthDisplay.textContent = `Strength: ${strength}`;
        });
    }
});


