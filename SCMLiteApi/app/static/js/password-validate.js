function validatePassword() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("cpassword").value;
  const message = document.getElementById("passwordMessage");

  if (password !== confirmPassword) {
    message.innerHTML = "Passwords do not match";
    message.style.color = "red";
  } else {
    message.innerHTML = "Passwords match";
    message.style.color = "green";
  }
}

function showPassword() {
  const passwordInput = document.getElementById("password");
  const showPasswordButton = document.getElementById("showPassword");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    showPasswordButton.innerHTML = "HIDE";
  } else {
    passwordInput.type = "password";
    showPasswordButton.innerHTML = "SHOW";
  }
}

function validateForm() {
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("cpassword").value;

  if (password !== confirmPassword) {
    alert("Passwords do not match");
    return false;
  } else {
    return true;
  }
}

document.getElementById("showPassword").addEventListener("click", showPassword);
document.getElementById("cpassword").addEventListener("keyup", validatePassword);
