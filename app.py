from flask import Flask, render_template, request, jsonify
import json
import base64
import re
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from flask_cors import CORS
import json
from youtubesearchpython import VideosSearch

sysprompt = """
Task: Generate 3 complete recipes from an image containing various food ingredients. The recipes should utilize all identified ingredients and provide detailed instructions for preparation and cooking.

Input: <image>

Instructions:
1. Analyze the input image to identify and extract all food ingredients present.
2. Return a json formatted string with only the identified ingredients actually present in the image, 4 names of recipes a person can make with them.
Output Format
{
  "ingredients": [
    "(only the ingredient or ingredients actually present in the given image)"
  ],
  "recipes": [
    "<recipe name 1>",
    "<recipe name 2>",
    "<recipe name 3>",
    "<recipe name 4>"
  ]
}
If it is not an image of ingredients:
output format:
{
    error:"Not an image of ingredients!"
}
keep these extra instructions in mind and choose a recipe from the given cuisine,type and diet accordingly (if any) :
"""

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY = "AIzaSyCDiikf5hI17vKD0M9j06H5g6FxRcBzVVA"

genai.configure(api_key=GOOGLE_API_KEY)

gemini = genai.GenerativeModel('gemini-pro-vision')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/generate_recipe')
def generate_recipe():
    return render_template('generate_recipe.html')

@app.route('/gen', methods=['POST'])
def gen():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image data'}), 400

    if request.form.get('extras'):
        prompt = sysprompt + request.form.get('extras').replace('{', '').replace('}', '').replace('"', '')
    else:
        prompt = sysprompt

    image_file = request.files['image']
    image_bytes = image_file.read()
    image_pil = Image.open(BytesIO(image_bytes))
    res = gemini.generate_content([prompt, image_pil])
    res.resolve()

    # Find the first and last { } in the response text
    start_index = res.text.find('{')
    end_index = res.text.rfind('}') + 1

    if start_index == -1 or end_index == -1:
        return jsonify({'error': 'Failed to parse recipe JSON'}), 400

    # Extract the JSON-like string
    json_like_str = res.text[start_index:end_index]

    try:
        # Parse the JSON-like string to a dictionary
        response_dict = json.loads(json_like_str)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid input'}), 400

    # Extract ingredients and recipe names
    ingredients = response_dict.get('ingredients', [])
    recipe_names = response_dict.get('recipes', [])

    # Fetch the YouTube video for each recipe
    recipes = []
    for recipe_name in recipe_names:
        videosSearch = VideosSearch(recipe_name + ' recipe', limit=1)
        recipe_video = videosSearch.result()['result'][0]['link'].replace('watch?v=', 'embed/')
        recipes.append({
            'name': recipe_name,
            'youtube_video': recipe_video
        })

    # Construct the final JSON response
    output = {
        'ingredients': ingredients,
        'recipes': recipes
    }
    print(output)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)