window.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registerUser');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');

    form.addEventListener('submit', function(event) {
        if (passwordInput.value !== confirmPasswordInput.value) {
            event.preventDefault();
            alert('Passwords do not match!');
        }
    });
});