
document.getElementById('login-form').addEventListener('submit', function(e) {
  e.preventDefault();
  var passwordInput = document.getElementById('password');
  var password = passwordInput.value;

  if (password.length < 8) {
    var errorDiv = document.getElementById('password-error');
    errorDiv.textContent = "Password must be at least 8 characters long.";
    return;
  }

  if (password.length > 12) {
    var errorDiv = document.getElementById('password-error');
    errorDiv.textContent = "Password must be at most 12 characters long.";
    return;
  }

  
});
function togglePassword() {
  var passwordField = document.getElementById("password");
  var eyeIcon = document.getElementById("toggleEye");
  if (passwordField.type === "password") {
      passwordField.type = "text";
      eyeIcon.src = "{% static 'Images/Eye Open.png' %}"; // Path to the slashed eye image
  } else {
      passwordField.type = "password";
      eyeIcon.src = "{% static 'Images/Eye.png' %}"; // Path to the eye image
  }
}

