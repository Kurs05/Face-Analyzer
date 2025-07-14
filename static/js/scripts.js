 const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileElem');
    const uploadBtn = document.querySelector('.upload-btn');

    dropArea.addEventListener('click', () => fileInput.click());
    uploadBtn.addEventListener('click', () => fileInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => {
            e.preventDefault();
            dropArea.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, e => {
            e.preventDefault();
            dropArea.classList.remove('dragover');
        });
    });

    dropArea.addEventListener('drop', e => {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
        }
    });

