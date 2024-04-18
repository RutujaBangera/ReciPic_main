let popup = document.getElementById("popup");
function openPopup(){
    popup.classList.add("open-popup");
}
function closePopup(){
    popup.classList.remove("open-popup");
}
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
  <div class="card mb-4">
    <div class="card-body">
      <h5 class="card-title">Identified Ingredients</h5>
      <ul>
        ${response.ingredients.map(ingredient => `<li>${ingredient}</li>`).join('')}
      </ul>
    </div>
  </div>
  ${response.recipes.map(recipe => `
    <div class="card mb-4">
      <div class="card-body">
        <h5 class="card-title">${recipe.name}</h5>
        <div class="embed-responsive embed-responsive-16by9">
          <iframe class="embed-responsive-item" src="${recipe.youtube_video}" allowfullscreen></iframe>
        </div>
      </div>
    </div>
  `).join('')}
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
