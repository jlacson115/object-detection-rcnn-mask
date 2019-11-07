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
    imgFilename = input_params[input_params.rfind("/")+1:]
    imgFilename = imgFilename.replace("jpeg", "png")
    imgFilename = imgFilename.replace("jpg", "png")
    
    s3 = boto3.resource("s3")
    object = s3.Object(PUBLIC_BUCKET, imgFilename)
    object.upload_fileobj(file_object)
    
    
    s3Url = "https://"+ PUBLIC_BUCKET +".s3.us-east-2.amazonaws.com/" + imgFilename
    
    data = {
        "detectedUrl" : s3Url
    }

    #return send_file(file_object, mimetype='application/json')
    return data;
    
@app.route('/hello', methods=['GET'])
def hi():
    return "hi"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
    
