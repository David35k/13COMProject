$(document).ready(function () {
    $('.like-button').on('click', function (event) {
        id = this.id;
        $.ajax({
            url: '/post/like?postID=' + id,
            type: 'GET',
            success: function (response) {
                document.getElementsByClassName(id)[0].innerHTML = response;
            }
        });
    });
});