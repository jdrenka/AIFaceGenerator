from flask import Flask, send_file
import main as main # Import GAN script
import torch
from torchvision.utils import save_image
from main import Generator
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

generator = Generator()
generator.load_state_dict(torch.load('generator_model.pth'))
generator.eval()  # Set to eval mode for inference


@app.route('/generate-image')
def generate_image():
    # Generate an image with the loaded model
    # Noise vector for generator
    noise = torch.randn(1, 100)

    # Scale the noise vector by a factor
    scaled_noise = noise * 2.0   

    with torch.no_grad():
        generated_image = generator(scaled_noise)

    # Save the generated image to a temporary file and send it
    filepath = 'temp_image.png'  # Consider using a temp file or dynamic naming to handle concurrency
    save_image(generated_image, filepath)  # `save_image` from torchvision or similar utility
    return send_file(filepath, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)