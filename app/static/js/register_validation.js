document.addEventListener("DOMContentLoaded", function() {
    const usernameField = document.getElementById('username');
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirmPassword');
    const usernameFeedback = document.getElementById('usernameFeedback');
    const passwordFeedback = document.getElementById('passwordFeedback');
    const confirmPasswordFeedback = document.getElementById('confirmPasswordFeedback');

    usernameField.addEventListener('blur', checkUsernameAvailability);
    passwordField.addEventListener('input', validatePassword);
    confirmPasswordField.addEventListener('input', validateConfirmPassword);

    function checkUsernameAvailability() {
        const username = usernameField.value;
        console.log('Checking username availability for:', username);  // 调试输出
        fetch(`/auth/check_username?username=${username}`)
            .then(response => response.json())
            .then(data => {
                console.log('Username availability response:', data);  // 调试输出
                if (data.available) {
                    usernameField.classList.remove('is-invalid');
                    usernameField.classList.add('is-valid');
                    usernameFeedback.textContent = 'Username is available';  // 更新反馈文本
                    usernameFeedback.classList.remove('invalid-feedback');
                    usernameFeedback.classList.add('valid-feedback');
                } else {
                    usernameField.classList.remove('is-valid');
                    usernameField.classList.add('is-invalid');
                    usernameFeedback.textContent = 'Username already taken. Please choose another one.';
                    usernameFeedback.classList.remove('valid-feedback');
                    usernameFeedback.classList.add('invalid-feedback');
                }
            })
            .catch(error => console.error('Error:', error));
    }

    function validatePassword() {
        const password = passwordField.value;
        const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,20}$/;
        if (passwordPattern.test(password)) {
            passwordField.classList.remove('is-invalid');
            passwordField.classList.add('is-valid');
            passwordFeedback.textContent = '';
        } else {
            passwordField.classList.remove('is-valid');
            passwordField.classList.add('is-invalid');
            passwordFeedback.textContent = 'Password must be 8-20 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.';
        }
        validateConfirmPassword(); // Ensure confirm password is also validated whenever the password changes
    }

    function validateConfirmPassword() {
        const password = passwordField.value;
        const confirmPassword = confirmPasswordField.value;
        if (password === confirmPassword) {
            confirmPasswordField.classList.remove('is-invalid');
            confirmPasswordField.classList.add('is-valid');
            confirmPasswordFeedback.textContent = '';
        } else {
            confirmPasswordField.classList.remove('is-valid');
            confirmPasswordField.classList.add('is-invalid');
            confirmPasswordFeedback.textContent = 'Passwords do not match.';
        }
    }
});
