from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from PIL import Image
import io
import predict
import boto3

PUBLIC_BUCKET = "object-detect-image-website"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/predict": {"origins": "*"}})

@app.route('/predict', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def run():
    data = request.get_json(force=True)
    input_params = data['input']
    file_object = predict.predict(input_params)
    
    s3 = boto3.resource("s3")
    object = s3.Object(PUBLIC_BUCKET, 'image.png')
    object.upload_fileobj(file_object)

    return send_file(file_object, mimetype='image/PNG')
    
@app.route('/hello', methods=['GET'])
def hi():
    return "hi"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
