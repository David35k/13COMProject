document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('comment-form');
    const commentField = document.getElementById('comment');

    commentField.addEventListener('input', function () {
        validateCommentField(commentField);
    });

    form.addEventListener('submit', function (event) {
        if (!validateCommentField(commentField)) {
            event.preventDefault();
        }
    });

    function validateCommentField(input) {
        let errorMessageElement = document.getElementById('comment-error');
        if (!errorMessageElement) {
            errorMessageElement = document.createElement('div');
            errorMessageElement.id = 'comment-error';
            errorMessageElement.className = 'error-message';
            input.parentNode.appendChild(errorMessageElement);
        }

        const value = input.value.trim();
        if (value === '') {
            errorMessageElement.textContent = "Can't submit empty comment";
            return false;
        } else if (input.value.includes('\n')) {
            errorMessageElement.textContent = 'Comment cannot contain newline characters.';
            return false;
        } else {
            errorMessageElement.textContent = '';
            return true;
        }
    }
});
