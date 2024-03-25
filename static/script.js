function uploadImage(event) {
  const file = event.target.files[0];
  const formData = new FormData();
  formData.append("image", file);
  document.getElementById("recipe-container").innerHTML =
    '<h3 style="color:white;">Generating...</h3>';
  // Replace the following URL with the server endpoint to handle image upload
  fetch("/gen", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((response) => {
      if (response.error) {
        document.getElementById(
          "recipe-container"
        ).innerHTML = `<h1>${response.error}</h1>`;
      } else {
        const recipeHTML = `
      <h2>${response.name}</h2>
      <h3>Ingredients</h3>
      <ul>
        ${response.ingredients
          .map((ingredient) => `<li>${ingredient}</li>`)
          .join("")}
      </ul>
      <h3>Preparation</h3>
      <ol>
        ${response.preparation.map((step) => `<li>${step}</li>`).join("")}
      </ol>
      <h3>Serving</h3>
      <ul>
      ${response.serving.map((suggestion) => `<li>${suggestion}</li>`).join("")}
      </ul>
      <h3>Notes</h3>
      <ul>
        ${response.notes.map((note) => `<li>${note}</li>`).join("")}
      </ul>
    `;

        document.getElementById("recipe-container").innerHTML = recipeHTML;
      }
    })
    .catch((error) => {
      console.error("Error uploading image:", error);
    });
}
