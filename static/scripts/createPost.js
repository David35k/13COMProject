// script.js
document.addEventListener('DOMContentLoaded', () => {
    const tagInput = document.getElementById('tag-input');
    const tagContainer = document.getElementById('tag-container');
    const tagListInput = document.getElementById('tag-list');
    let tags = [];

    tagInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const tag = tagInput.value.trim();
            if (tag && !tags.includes(tag)) {
                tags.push(tag);
                tagInput.value = '';
                updateTagDisplay();
                updateTagListInput();
            }
        }
    });

    function updateTagDisplay() {
        tagContainer.innerHTML = '';
        tags.forEach(tag => {
            const tagElement = document.createElement('div');
            tagElement.className = 'tag';
            tagElement.innerHTML = `<span>${tag}</span><span class="remove-tag">&times;</span>`;
            tagElement.querySelector('.remove-tag').addEventListener('click', () => {
                tags = tags.filter(t => t !== tag);
                updateTagDisplay();
                updateTagListInput();
            });
            tagContainer.appendChild(tagElement);
        });
    }

    function updateTagListInput() {
        tagListInput.value = tags.join(',');
    }
});