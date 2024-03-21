from flask import Flask, render_template, request, jsonify
import json
import base64
import re
from PIL import Image
from io import BytesIO
import google.generativeai as genai
from flask_cors import CORS

prompt = """
You are a highly capable AI assistant with advanced computer vision capabilities. Your task is to analyze an image and identify all the ingredients present in the image. Once you have identified the ingredients, you will generate a recipe using only those ingredients.
Return html for the following
Here are the steps you should follow:

1. Analyze the image carefully and identify all the ingredients present. Make a list of the ingredients.

2. If you are unsure about any items in the image, list them separately and indicate your uncertainty.

3. Once you have the list of ingredients, generate a recipe that uses only those ingredients. The recipe should be clear, concise, and easy to follow.

4. If there are any uncommon or specialized ingredients in the list, provide a brief explanation or description of those ingredients.

5. The recipe should include the following sections:
   - Ingredients list (with quantities)
   - Preparation instructions (step-by-step)
   - Cooking instructions
   - Serving suggestions (if applicable)

6. If there are any dietary restrictions or preferences that can be accommodated based on the ingredients, mention them and provide alternatives or modifications where possible.

7. Provide a name or title for the recipe that accurately represents the dish.

8. If there are any potential challenges or limitations in creating a recipe with the given ingredients, mention them and suggest possible solutions or alternatives.

Remember, your goal is to create a delicious and practical recipe using only the ingredients identified from the image. Be creative, but also ensure that the recipe is realistic and easy to follow for someone with basic cooking skills.
"""

app = Flask(__name__)
CORS(app)

GOOGLE_API_KEY="AIzaSyCDiikf5hI17vKD0M9j06H5g6FxRcBzVVA"

genai.configure(api_key=GOOGLE_API_KEY)

gemini = genai.GenerativeModel('gemini-pro-vision')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_recipe')
def generate_recipe():
    return render_template('generate_recipe.html')
@app.route('/gen', methods=['POST'])
def gen():
    if 'image' not in request.files:
        return jsonify({'error': 'Missing image data'}), 400

    image_file = request.files['image']
    image_bytes = image_file.read()
    image_pil = Image.open(BytesIO(image_bytes))

    res = gemini.generate_content([prompt, image_pil])
    res.resolve()

    recipe = res.text.replace('\n', '')

    return jsonify({'res': recipe})

if __name__ == '__main__':
    app.run(debug=True)
