document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('upload-form');
    const imageInput = document.getElementById('image-input');
    const resultDiv = document.getElementById('result');
    const colorList = document.getElementById('color-list');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append('file', imageInput.files[0]);

        fetch('/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            resultDiv.classList.remove('hidden');
            colorList.innerHTML = '';
            data.forEach(color => {
                const li = document.createElement('li');
                li.style.backgroundColor = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
                li.innerText = `RGB: (${color[0]}, ${color[1]}, ${color[2]})`;
                colorList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
