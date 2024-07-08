document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('fileInput').addEventListener('change', function (event) {
        const file = event.target.files[0];
        const preview = document.getElementById('image-preview');

        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
            reader.readAsDataURL(file);
        } else {
            preview.style.display = 'none';
        }
    });

    document.getElementById('clearButton').addEventListener('click', function () {
        console.log("ohio");
        console.log(document.getElementById('fileInput').value);
        document.getElementById('fileInput').value = '';
        console.log(document.getElementById('fileInput').value);


        // Hide the preview image
        const preview = document.getElementById('image-preview');
        preview.src = '';
        preview.style.display = 'none';
    });
});