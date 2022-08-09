var fileInput = document.querySelector('#file-box');
const textbox = document.querySelector('.file-name-textbox')

fileInput.addEventListener('change', showFileName);

function showFileName(event) {
    var fileInfoArea = document.querySelectorAll('.uploaded-file-name')
    var input = event.srcElement;
    var fileName = input.files[0].name;

    if (fileInfoArea.length == 0) {
        fileInfoArea = document.createElement('div');
        fileInfoArea.classList.add('uploaded-file-name');
        fileInfoArea.textContent = 'File name: ' + fileName;
        textbox.appendChild(fileInfoArea)
    } else {
        fileInfoArea = fileInfoArea[0]
    }
    fileInfoArea.textContent = 'File name: ' + fileName;
}