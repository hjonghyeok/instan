function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function(){
        const output = document.getElementById('preview');
        output.src = reader.result;
        document.getElementById('submit-button').disabled = false;
    };
    reader.readAsDataURL(event.target.files[0]);
}

document.getElementById('comment-input').addEventListener('input', function() {
    const comment = this.value.trim();
    const fileInput = document.getElementById('file-input').files.length > 0;
    document.getElementById('submit-button').disabled = !(comment && fileInput);
});