document.addEventListener('DOMContentLoaded', function () {
    const imgSelect = document.getElementById(imageId);
    console.log(srcImg)

    const preview = document.getElementById('preview')
    imgSelect.addEventListener('change', () => {
        const [file] = imgSelect.files
        if (file) {
            preview.src = URL.createObjectURL(file)
        } else {
            preview.src = `/media/${srcImg}`;
        }
    })

});