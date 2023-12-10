// script from https://medium.com/geekculture/how-to-preview-images-before-upload-with-javascript-3420e3cd2f1c
// Allow for previewing a photo before creating a post
const p = document.getElementById('preview')
const input = document.getElementById('image');
const previewPhoto = () => {
    const file = input.files;
    if (file) {
        const fileReader = new FileReader();

        p.innerHTML = ''
        let img = document.createElement('img')
        img.setAttribute('id', 'community-image')
        img.classList.add('preview')
        img.classList.add('border')
        img.classList.add('border-1')

        p.appendChild(img)
fileReader.onload = function (event) {
            img.setAttribute('src', event.target.result);
        }
        fileReader.readAsDataURL(file[0]);
    }
}
input.addEventListener("change", previewPhoto);