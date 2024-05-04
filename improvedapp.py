from flask import Flask, render_template, request, jsonify
import json
import base64
import re
from PIL import Image
from io import BytesIO
from flask_cors import CORS
import json
from youtubesearchpython import VideosSearch
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "vikhyatk/moondream2"
revision = "2024-04-02"


dream_model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision,
    torch_dtype=torch.bfloat16,
).cuda()
dream_tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)


gemma_tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
gemma_model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2b-it",
    device_map="auto",
    torch_dtype=torch.bfloat16,
)


app = Flask(__name__)
CORS(app)



def extract_json(sentence):
    bindex = sentence.index('model')
    sliced_string = sentence[bindex+5:]
    if sliced_string[sliced_string.rfind('<eos>')-1] == '}':
        sliced_string = sliced_string[sliced_string.index('{') : (sliced_string.rfind('}')) + 1]
    else :
        sliced_string = sliced_string[sliced_string.index('{'):sliced_string.rfind('<eos>')] + '}]}'
    print(sliced_string)
    return sliced_string.replace('\n','')

def get_recipe(image, instructions=""):
    enc_image = dream_model.encode_image(image)
    dream_out = dream_model.answer_question(enc_image, "Analyze the image, are there any food ingredients in this image if yes, list them including the names of fruits, vegetables, spices, meat, if they exist and describe them", dream_tokenizer)
    prompt = f"""
   <bos><start_of_turn>user
    {dream_out}
From the above information about food ingredients, analyze the ingredients and suggest 3 recipes with descriptions for beginners that we can make with only these ingredients and nothing else.
Keep in mind these extra instructions: {instructions}
Return your response in the following JSON format:

{{
    "ingredients": [
        "list of ingredients"
    ],
    "recipes": [
        {{
            "name": "Recipe 1 Name",
            "ingredients": [
                "list of ingredients for recipe 1"
            ],
            "description": "Recipe 1 description"
        }},
        {{
            "name": "Recipe 2 Name",
            "ingredients": [
                "list of ingredients for recipe 2"
            ],
            "description": "Recipe 2 description"
        }},
        {{
            "name": "Recipe 3 Name",
            "ingredients": [
                "list of ingredients for recipe 3"
            ],
            "description": "Recipe 3 description"
        }}
    ]
}}
** ensuring that the json is structured and terminated properly is extremely important **
<end_of_turn>
<start_of_turn>model
"""

    input_ids = gemma_tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = gemma_model.generate(**input_ids, max_new_tokens=2000)
    outputs = gemma_tokenizer.decode(outputs[0])
    print(outputs)
    jsonout = extract_json(sentence=outputs)
    return json.loads(jsonout) 

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

    

    image_file = request.files['image']
    image_bytes = image_file.read()
    image_pil = Image.open(BytesIO(image_bytes))


    try:
        if request.form.get('extras'):
            response_dict = get_recipe(image_pil,request.form.get('extras').replace('{', '').replace('}', '').replace('"', ''))
        else:
            response_dict = get_recipe(image_pil)

    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'Invalid input'}), 400

    # Extract ingredients and recipe names
    ingredients = response_dict.get('ingredients', [])
    recipes = response_dict.get('recipes', [])
    print(recipes)
    # Fetch the YouTube video for each recipe
    recipe_list = []
    for recipe in recipes:
        videosSearch = VideosSearch(recipe['name'] + ' recipe', limit=1)
        recipe_video = videosSearch.result()['result'][0]['link'].replace('watch?v=', 'embed/')
        recipe_list.append({
            'name': recipe['name'],
            'description' : recipe['description'],
            'ingredients' : recipe['ingredients'],
            'youtube_video': recipe_video,
        })

    # Construct the final JSON response
    output = {
        'ingredients': ingredients,
        'recipes': recipe_list
    }
    print(output)
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)