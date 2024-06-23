// script.js
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');

fileInput.addEventListener('change', () => {
    const files = fileInput.files;
    handleFiles(files);
});

function handleFiles(files) {
    files = [...files];
    files.forEach(previewFile);
}

function previewFile(file) {
    const reader = new FileReader();
    reader.readAsDataURL(file);

    reader.onloadend = () => {
        const img = document.createElement('img');
        img.src = reader.result;
        preview.innerHTML = '';
        preview.appendChild(img);
    }
}
