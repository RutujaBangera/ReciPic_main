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
Task: Generate a complete recipe from an image containing various food ingredients. The recipe should utilize all identified ingredients and provide detailed instructions for preparation and cooking.

Input: <image>

Instructions:
1. Analyze the input image to identify and extract all food ingredients present.
2. Generate a list of ingredients with quantities required for the recipe.
3. Create step-by-step preparation instructions for the dish.
4. Provide detailed cooking instructions, including temperatures and cooking times if applicable.
5. Suggest appropriate serving recommendations to enhance the dish.
6. Consider any dietary restrictions or preferences based on the ingredients and provide modifications if needed.
7. Address any potential challenges or limitations in creating the recipe from the given ingredients.
8. Output the full recipe in JSON format with the following sections:
    name : <name of the recipe> - string
    ingredients: <list ingredients with quantities> - array of strings
    preparation: <steps for preparation> - array of strings
    serving: <serving suggestion> - array of strings
    notes: <any additional notes, substitutions, challenges, etc.> - array of strings

Be creative in generating an appealing and practical recipe while ensuring it remains realistic based on the identified ingredients.
If it is not an image of ingredients, output {error:"Not an image of ingredients!"}
Output: <recipe in JSON format>

keep these extra instructions in mind and choose a recipe from the given cuisine,type and diet accordingly (if any) : 
"""

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY="AIzaSyCDiikf5hI17vKD0M9j06H5g6FxRcBzVVA"

genai.configure(api_key=GOOGLE_API_KEY)

gemini = genai.GenerativeModel('gemini-pro-vision')


@app.route('/')
def index():
    return render_template('index.html')

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
        prompt = sysprompt + request.form.get('extras').replace('{','').replace('}','').replace('"','')
    else:
        prompt = sysprompt
    image_file = request.files['image']
    image_bytes = image_file.read()
    image_pil = Image.open(BytesIO(image_bytes))

    res = gemini.generate_content([prompt, image_pil])
    res.resolve()

    recipe = res.text
    # Find the first '{' and the last '}' in the response
    first_brace_index = recipe.find('{')
    last_brace_index = recipe.rfind('}')
    
    if first_brace_index == -1 or last_brace_index == -1:
        return jsonify({'error': 'Invalid recipe format'}), 400

    # Extract the JSON string from the response
    json_string = recipe[first_brace_index:last_brace_index+1]
    
    try:
        # Convert the JSON string to a JSON object
        recipe_json = json.loads(json_string)
        if recipe_json['error']:
                return jsonify(recipe_json), 400
        
        videosSearch = VideosSearch(recipe_json['name'], limit = 1)
        recipe_json['youtube_video'] = videosSearch.result()['result'][0]['link'].replace('watch?v=','embed/')
    except json.JSONDecodeError:
        return jsonify({'error': 'Failed to parse recipe JSON'}), 400
    
    return jsonify(recipe_json)

if __name__ == '__main__':
    app.run(debug=True)
