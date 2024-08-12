document.addEventListener('DOMContentLoaded', function () {
    const limits = {
        name: 30,
        userName: 30,
        email: 255,
        password: 8 // Minimum length for the password
    };

    const form = document.getElementById('epicForm');
    const fields = ['name', 'userName', 'email', 'password'];

    const validFileExtensions = [".jpg", ".jpeg", ".bmp", ".gif", ".png"];

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

        const fileInput = document.getElementById('fileInput');

        // if (fileInput.files.length === 0 && form.classList.contains("epic")) {
        //     let errorMessageElement = document.getElementById('fileInput-error');
        //     if (!errorMessageElement) {
        //         errorMessageElement = document.createElement('div');
        //         errorMessageElement.id = 'fileInput-error';
        //         errorMessageElement.className = 'error-message';
        //         fileInput.parentNode.appendChild(errorMessageElement);
        //         errorMessageElement.textContent = 'Image is required.';
        //     }

        //     valid = false;
        // } else if (fileInput.files.length === 0) {

        // }

        // some random stuff for file extension WIP
        // for (let j = 0; j < validFileExtensions.length; j++) {
        //     let sCurExtension = validFileExtensions[j];
        //     if (sFileName.substr(sFileName.length - sCurExtension.length, sCurExtension.length).toLowerCase() == sCurExtension.toLowerCase()) {
        //         blnValid = true;
        //         break;
        //     }
        // }

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
            alert("The form you tried to submit has some invalid fields. Please change them before submitting.");
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

        if (fieldName === 'userName' || fieldName === 'email') {
            checkFieldInDatabase(fieldName, input.value, function (exists) {
                if (exists) {
                    isValid = false;
                    errorMessage = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is already taken.`;
                }
                document.getElementById(fieldName + '-error').textContent = isValid ? '' : errorMessage;
            });
        }

        document.getElementById(fieldName + '-error').textContent = isValid ? '' : errorMessage;
        return isValid;
    }

    function checkFieldInDatabase(field, value, callback) {
        fetch('/check_field', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ field: field, value: value })
        })
            .then(response => response.json())
            .then(data => {
                callback(data.exists);
            })
            .catch(error => {
                console.error('Error:', error);
                callback(false);
            });
    }
});