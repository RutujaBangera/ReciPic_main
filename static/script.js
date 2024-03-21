function uploadImage(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('image', file);

    // Replace the following URL with the server endpoint to handle image upload
    fetch('/gen', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data['res'])
        const recipeContainer = document.getElementById('recipe-container');
        recipeContainer.innerHTML = data['res'];
    })
    .catch(error => {
        console.error('Error uploading image:', error);
    });
}