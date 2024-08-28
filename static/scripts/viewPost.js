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
        console.log(value.length)
        if (value === '') {
            errorMessageElement.textContent = "Can't submit empty comment";
            return false;
        } else if (value.includes('\n')) {
            errorMessageElement.textContent = 'Comment cannot contain newline characters.';
            return false;
        } else if (value.length > 5000) {
            errorMessageElement.textContent = 'Comment cannot be longer than 1000 characters! Why do you need to write so much anyway?';
            return false;
        }
        else {
            errorMessageElement.textContent = '';
            return true;
        }
    }
});

$(document).ready(function () {
    $('.like-button').on('click', function (event) {
        id = this.id;
        $.ajax({
            url: '/comment/like?commentID=' + id,
            type: 'GET',
            success: function (response) {
                document.getElementsByClassName(id)[0].innerHTML = response;
            }
        });
    });
});
