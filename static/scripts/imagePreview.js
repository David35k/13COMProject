document.addEventListener('DOMContentLoaded', function () {

    fileInput = document.getElementById('fileInput');
    const validImageTypes = ['image/jpeg', 'image/png', 'image/gif'];

    fileInput.addEventListener('change', function (event) {
        const file = event.target.files[0];
        const fileType = file['type'];
        const preview = document.getElementById('image-preview');

        if (file) {
            if (!validImageTypes.includes(fileType)) {
                alert('Please upload a valid image file (JPEG, PNG, or GIF).');
                this.value = ''; // Clear the input
                return;
            }

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
        console.log(fileInput.value);
        fileInput.value = '';
        console.log(fileInput.value);

        // Hide the preview image
        const preview = document.getElementById('image-preview');
        preview.src = '';
        preview.style.display = 'none';
    });

    document.getElementById('anotherClearButton').addEventListener('click', function () {
        console.log("OHIO");
        console.log(fileInput.value);
        document.getElementById("usePlaceholder").value = 1;
        console.log(fileInput.value);
        console.log(document.getElementById("usePlaceholder").value);

        // Hide the preview image
        const preview = document.getElementById('image-preview');
        preview.src = '/static/images/websiteImages/pfpPlaceholder.jpg';
        preview.style.display = 'block';
    });
});