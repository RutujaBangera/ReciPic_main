// Include jQuery library
extras = {}
$('.btn-filter').on('click', function() {
  const category = $(this).find('input').attr('name');
  const buttonId = $(this).find('input').attr('id');

  // If the button is active, remove its property from extras
  if ($(this).hasClass('active')) {
    console.log('active');
    $(this).removeClass('active');
    delete extras[category];
  } else {
    console.log('inactive');
    // If the button is inactive, add its property to extras
    extras[category] = buttonId;
    $(this).addClass('active').siblings().removeClass('active');
  }

  console.log(extras);
});


function uploadImage(event) {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append("image", file);
  formData.append("extras", JSON.stringify(extras));
  document.getElementById('loading-gif').style.display = 'flex'
  // Replace the following URL with the server endpoint to handle image upload
  fetch("/gen", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      document.getElementById('loading-gif').style.display = 'None'
      if (response.error) {
        document.getElementById(
          "recipe-container"
        ).innerHTML = `<h1>${response.error}</h1>`;
      } else {
        const recipeHTML = `
        <div class="container">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title">${response.name}</h2>
            <h3 class="my-3">Ingredients</h3>
            <ul class="list-group">
              ${response.ingredients.map(ingredient => `
                <li class="list-group-item">${ingredient}</li>
              `).join('')}
            </ul>
            <h3 class="my-3">Preparation</h3>
            <ol class="list-group list-group-numbered">
              ${response.preparation.map(step => `
                <li class="list-group-item">${step}</li>
              `).join('')}
            </ol>
            <h3 class="my-3">Serving</h3>
            <ul class="list-group">
              ${response.serving.map(suggestion => `
                <li class="list-group-item">${suggestion}</li>
              `).join('')}
            </ul>
            <h3 class="my-3">Notes</h3>
            <ul class="list-group">
              ${response.notes.map(note => `
                <li class="list-group-item">${note}</li>
              `).join('')}
            </ul>
          </div>
        </div>
      </div>
`;


        document.getElementById("recipe-container").innerHTML = recipeHTML;
        document.getElementById('home-content').style.display = 'None';
        document.getElementById('filter-card').style.display = 'None';
        
      }
    })
    .catch((error) => {
      console.error("Error uploading image:", error);
    });
}
