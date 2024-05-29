from flask import Flask, request, render_template, flash, send_file,jsonify, send_from_directory,send_from_directory,url_for
import numpy as np
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
import secrets



app = Flask(__name__)


def generate_image(prompt):
    # Assuming `pipe` is defined somewhere in your code
    image = np.array(pipe(prompt=prompt).images[0])
    return image

@app.route('/generate', methods=['POST'])
def generate():
    text = request.json['text']
    image = generate_image(text)
    # Convert the NumPy array to a PIL Image
    pil_image = Image.fromarray(image)
    # Save the PIL Image in the static directory
    random_string = secrets.token_hex(8)
    filename = f'static/generated_{random_string}.png'
    pil_image.save(filename)
    # Generate the URL for the image
    url = url_for('static', filename=f'generated_{random_string}.png')
    # Return the URL as a JSON response
    return jsonify({'image_url': url})

@app.route('/')
def index():
    return send_from_directory('.','index.html')

app.run(host="0.0.0.0", port=5000)
