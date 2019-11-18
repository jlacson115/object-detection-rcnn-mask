from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin
from PIL import Image
import io
import predict
import boto3

PUBLIC_BUCKET = "object-detect-image-website"
PUBLIC_FOLDER = "detections/"

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
    
    # video frames are output to /detections/REQ_ID/frame.jpg
    # uploaded images are output to /uploads/IMAGE.jpg
    
    if input_params.find("/detections/") < 0 :
        # it's an image
        imgFilename = input_params[input_params.rfind("/")+1:]
        imgFilename = imgFilename.replace("jpeg", "png")
        imgFilename = imgFilename.replace("jpg", "png")
        out_filename = PUBLIC_FOLDER + imgFilename
    else:
    	# its a video
    	frameFilename = input_params[input_params.find("/detections/"):]
        frameFilename = frameFilename.replace("jpg", "png")
        out_filename = frameFilename
    
    s3 = boto3.resource("s3")
    object = s3.Object(PUBLIC_BUCKET, out_filename)
    object.upload_fileobj(file_object)
    
    s3Url = "https://"+ PUBLIC_BUCKET +".s3.us-east-2.amazonaws.com/" +  out_filename
    
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
    
