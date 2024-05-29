from flask import Flask, request, jsonify, send_from_directory, url_for

app = Flask(__name__)

def generate_image(prompt):
    # Assuming `pipe` is defined somewhere in your code
    # You need to implement this function or replace it with your image generation logic
    return None

@app.route('/generate', methods=['POST'])
def generate():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text parameter is missing'}), 400
    
    image = generate_image(text)
    if not image:
        return jsonify({'error': 'Failed to generate image'}), 500

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
    return send_from_directory('.', 'index.html')

if __name__ == "__main__":
    app.run(debug=False)
