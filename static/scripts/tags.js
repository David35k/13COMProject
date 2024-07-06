document.addEventListener('DOMContentLoaded', () => {
    const tagInput = document.getElementById('tag-input');
    const tagContainer = document.getElementById('tag-container');
    const tagListInput = document.getElementById('tag-list');
    const tagError = document.createElement('div');
    tagError.id = 'tag-error';
    tagError.className = 'error-message';
    tagInput.parentNode.appendChild(tagError);
    let tags = [];

    const TAG_LIMIT = 25;

    tagInput.addEventListener('input', () => {
        const tag = tagInput.value.trim();
        if (tag.length > TAG_LIMIT) {
            tagError.textContent = `Each tag cannot exceed ${TAG_LIMIT} characters.`;
        } else {
            tagError.textContent = '';
        }
    });

    tagInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            event.preventDefault();
            const tag = tagInput.value.trim();
            if (tag) {
                if (tag.length > TAG_LIMIT) {
                    tagError.textContent = `Each tag cannot exceed ${TAG_LIMIT} characters.`;
                } else if (!tags.includes(tag)) {
                    tags.push(tag);
                    tagInput.value = '';
                    updateTagDisplay();
                    updateTagListInput();
                    tagError.textContent = ''; // Clear error message
                }
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
