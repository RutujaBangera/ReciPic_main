// script.js

// Get the search button and input field
const searchButton = document.querySelector('.primary-btn');
const searchInput = document.querySelector('#searchbar');

// Add a click event listener to the search button
searchButton.addEventListener('click', () => {
  const query = searchInput.value.trim();
  if (query) {
    fetchRecipes(query);
  }
});

// Function to fetch the recipes from the API
function fetchRecipes(query) {
  const apiUrl = `https://api.edamam.com/api/recipes/v2?type=public&q=${query}&app_id=118f431a&app_key=
  62a68ed6adf68b74cfd4963bd70ee2ca`;
  // Make the AJAX request using the Fetch API
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      // Clear the previous recipe cards
      const recipeContainer = document.querySelector('.recipe-container');
      recipeContainer.innerHTML = '';

      // Loop through the recipes and create the cards
      data.hits.forEach(hit => {
        const recipe = hit.recipe;
        const card = createRecipeCard(recipe);
        recipeContainer.appendChild(card);
      });
    })
    .catch(error => {
      console.error('Error fetching recipes:', error);
    });
}

// Function to create a recipe card
function createRecipeCard(recipe) {
  const card = document.createElement('div');
  card.classList.add('recipe-card');

  const image = document.createElement('img');
  image.src = recipe.image;
  image.alt = recipe.label;

  const title = document.createElement('h3');
  title.textContent = recipe.label;

  const source = document.createElement('p');
  source.textContent = `Source: ${recipe.source}`;

  const link = document.createElement('a');
  link.href = recipe.url;
  link.textContent = 'View Recipe';
  link.target = '_blank';

  card.appendChild(image);
  card.appendChild(title);
  card.appendChild(source);
  card.appendChild(link);

  return card;
}