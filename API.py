# app.py
from flask import Flask, request, render_template, flash, send_file,jsonify, send_from_directory
from sqlalchemy import create_engine, Column, String, Integer, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import tensorflow as tf
import numpy as np
from io import BytesIO
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline
import os
import matplotlib.pyplot as plt
import secrets
model = "dreamlike-art/dreamlike-diffusion-1.0"
pipe = StableDiffusionPipeline.from_pretrained(model, torch_dtype=torch.float16, use_safetensors=True)
pipe = pipe.to("cuda")
model = torch.load("E:/CodePractice/Flask/Final API/model.h5")

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
    # Save the PIL Image as a temporary file
    random_string = secrets.token_hex(8)
    filename = f'generated_{random_string}.png'
    #pil_image.save(filename)
    # Generate the URL for the image
    url = request.host_url + 'static/' + filename
    # Return the URL as a JSON response
    return jsonify({'image_url': url})

@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory('.', filename)

app.run(port=5000)
