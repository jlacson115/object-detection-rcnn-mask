from flask import Flask, request, jsonify, send_file
from PIL import Image
import io
import predict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def run():
    data = request.get_json(force=True)
    input_params = data['input']
    file_object = predict.predict(input_params)
    
    # convert numpy array to PIL Image
    #img = Image.fromarray(result.astype('uint8'))
    
    # create file-object in memory
    #file_object = io.BytesIO()

    # write PNG in file-object
    #img.save(file_object, 'PNG')

    # move to beginning of file so `send_file()` it will read from start    
    #file_object.seek(0)

    return send_file(file_object, mimetype='image/PNG')
    
@app.route('/hello', methods=['GET'])
def hi():
    return "hi"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)