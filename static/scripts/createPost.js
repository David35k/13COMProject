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

    document.getElementById('fileInput').addEventListener('change', function (event) {
        const file = event.target.files[0];
        const preview = document.getElementById('image-preview');

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            preview.style.display = 'none';
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

        if (input.value.length > limit) {
            errorMessageElement.textContent = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} cannot exceed ${limit} characters.`;
            return false;
        } else {
            errorMessageElement.textContent = '';
            return true;
        }
    }
});
