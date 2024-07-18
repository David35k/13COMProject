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

function copyFunc(postID) {
    var copyText = "localhost:5000/post/view?postID=" + postID;
    navigator.clipboard.writeText(copyText);

    var tooltip = document.getElementById("myTooltip" + postID);
    tooltip.innerHTML = "Copied: " + copyText;
}

function outFunc() {
    var tooltip = document.getElementById("myTooltip");
    tooltip.innerHTML = "Copy post link";
}