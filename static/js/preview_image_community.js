// script from https://medium.com/geekculture/how-to-preview-images-before-upload-with-javascript-3420e3cd2f1c
// Allow for previewing a photo before creating a community
const input = document.getElementById('image');
const previewPhoto = () => {
    const file = input.files;
    if (file) {
        const fileReader = new FileReader();
        const preview = document.getElementById('community-image');
fileReader.onload = function (event) {
            preview.setAttribute('src', event.target.result);
        }
        fileReader.readAsDataURL(file[0]);
    }
}
input.addEventListener("change", previewPhoto);
