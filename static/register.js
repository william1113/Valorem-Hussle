const nameInput = document.getElementById('name');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const confirmationPassword = document.getElementById('confirmPassword');
const submitButton = document.getElementById('submit');
const passwordMatchIndicator = document.getElementById('passwordMatchIndicator')

const  checkPasswordMatch = () =>  {
    if (passwordInput.value.length > 0 && passwordInput.value === confirmationPassword.value) {
        submitButton.disabled = false;
        passwordMatchIndicator.textContent = '✓';
        passwordMatchIndicator.className = 'password-match';
    } else {
        submitButton.disabled = true;
        passwordMatchIndicator.textContent = '✕';
        passwordMatchIndicator.className = 'password-mismatch';
    }
};

passwordInput.addEventListener('input', checkPasswordMatch);
confirmationPassword.addEventListener('input', checkPasswordMatch);

