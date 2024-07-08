document.addEventListener('DOMContentLoaded', function () {
    const limits = {
        name: 30,
        userName: 30,
        email: 255,
        password: 8 // Minimum length for the password
    };

    const form = document.getElementById('epicForm');
    const fields = ['name', 'userName', 'email', 'password'];

    fields.forEach(field => {
        const input = document.getElementById(field);
        if (input) {
            input.addEventListener('input', function () {
                validateField(input, field, limits[field]);
            });
        }
    });

    form.addEventListener('submit', function (event) {
        let valid = true;
        fields.forEach(field => {
            const input = document.getElementById(field);
            if (input) {
                if (!validateField(input, field, limits[field])) {
                    valid = false;
                }
            }
        });

        if (!valid) {
            event.preventDefault();
        }
    });

    function validateField(input, fieldName, limit) {
        const errorMessageElement = document.getElementById(fieldName + '-error');
        if (!errorMessageElement) {
            const newErrorElement = document.createElement('div');
            newErrorElement.id = fieldName + '-error';
            newErrorElement.className = 'error-message roboto-medium';
            input.parentNode.appendChild(newErrorElement);
        }

        let isValid = true;
        let errorMessage = '';

        if (fieldName === 'password') {
            const password = input.value;
            if (password.length < limit) {
                isValid = false;
                errorMessage = 'Password must be at least 8 characters long.';
            } else {
                const numberCount = (password.match(/\d/g) || []).length;
                const specialCharCount = (password.match(/[^a-zA-Z0-9]/g) || []).length;
                if (numberCount < 2) {
                    isValid = false;
                    errorMessage = 'Password must contain at least two numbers.';
                }
                if (specialCharCount < 1) {
                    isValid = false;
                    errorMessage = 'Password must contain at least one special character.';
                }
            }
        } else {
            if (input.value.trim().length === 0) {
                isValid = false;
                errorMessage = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required`;
            }
            if (input.value.length > limit) {
                isValid = false;
                errorMessage = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} cannot exceed ${limit} characters.`;
            }
        }

        document.getElementById(fieldName + '-error').textContent = isValid ? '' : errorMessage;
        return isValid;
    }
});