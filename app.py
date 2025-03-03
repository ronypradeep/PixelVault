from flask import Flask, request, send_file, jsonify, render_template
from PIL import Image
import io

app = Flask(__name__)

# Function to encode a message into an image
def encode_message(image, message):
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '11111110'  # End of message marker
    pixels = list(image.getdata())
    if len(binary_message) > len(pixels) * 3:
        raise ValueError("Message too long for image")
    index = 0
    for i in range(len(pixels)):
        pixel = list(pixels[i])
        for j in range(3):
            if index < len(binary_message):
                pixel[j] = pixel[j] & ~1 | int(binary_message[index])
                index += 1
        pixels[i] = tuple(pixel)
    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(pixels)
    return encoded_image

# Function to decode a message from an image
def decode_message(image):
    pixels = list(image.getdata())
    binary_message = ''
    for pixel in pixels:
        for value in pixel[:3]:
            binary_message += str(value & 1)
    message = ''
    i = 0
    while i + 8 <= len(binary_message):
        byte = binary_message[i:i+8]
        if byte == '11111110':
            break
        message += chr(int(byte, 2))
        i += 8
    return message

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    image_file = request.files['image']
    message = request.form['message']
    image = Image.open(image_file)
    encoded_image = encode_message(image, message)
    img_io = io.BytesIO()
    encoded_image.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route('/decode', methods=['POST'])
def decode():
    image_file = request.files['image']
    image = Image.open(image_file)
    decoded_message = decode_message(image)
    return jsonify({'message': decoded_message})

if __name__ == '__main__':
    app.run(debug=True)