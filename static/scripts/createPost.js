document.addEventListener('DOMContentLoaded', function () {
    const limits = {
        title: 40,
        description: 65535
    };

    const form = document.getElementById('form');
    const fields = ['title', 'description'];


    fields.forEach(field => {
        const input = document.getElementById(field);
        input.addEventListener('input', function () {
            validateField(input, field, limits[field]);
        });
    });

    form.addEventListener('submit', function (event) {
        let valid = true;

        // Validate file input (image)

        if (fileInput.files.length === 0 && !form.classList.contains("epic")) {
            let errorMessageElement = document.getElementById('fileInput-error');
            if (!errorMessageElement) {
                errorMessageElement = document.createElement('div');
                errorMessageElement.id = 'fileInput-error';
                errorMessageElement.className = 'error-message';
                fileInput.parentNode.appendChild(errorMessageElement);
                errorMessageElement.textContent = 'Image is required.';
            }

            valid = false;
        }

        fields.forEach(field => {
            const input = document.getElementById(field);
            if (!validateField(input, field, limits[field])) {
                valid = false;
            }
        });

        if (!valid) {
            event.preventDefault();
        }
    });

    function validateField(input, fieldName, limit) {
        let errorMessageElement = document.getElementById(fieldName + '-error');
        if (!errorMessageElement) {
            errorMessageElement = document.createElement('div');
            errorMessageElement.id = fieldName + '-error';
            errorMessageElement.className = 'error-message';
            input.parentNode.appendChild(errorMessageElement);
        }

        if (input.value.trim().length === 0) {
            errorMessageElement.textContent = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required.`;
            return false;
        } else if (input.value.length > limit) {
            errorMessageElement.textContent = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} cannot exceed ${limit} characters.`;
            return false;
        } else {
            errorMessageElement.textContent = '';
            return true;
        }
    }
});
