const authTrack = document.querySelector("#auth-track");

document.querySelectorAll("[data-switch]").forEach((button) => {
  button.addEventListener("click", () => {
    const showSignup = button.dataset.switch === "signup";
    authTrack.classList.toggle("is-signup", showSignup);
    document.querySelector(showSignup ? "#signup-name" : "#id_username").focus({
      preventScroll: true,
    });
  });
});

document.querySelectorAll(".password-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const password = document.getElementById(button.getAttribute("aria-controls"));
    const showPassword = password.type === "password";
    password.type = showPassword ? "text" : "password";
    button.setAttribute("aria-label", showPassword ? "Hide password" : "Show password");
  });
});
