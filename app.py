import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import pickle5 as pickle
import json
from image_classification.util.util import get_hog_features, label_decode

UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template('upload.html')


@app.route('/predictions', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        response = app.response_class(
            response=json.dumps({'message': 'No file part'}),
            status=422,
            mimetype='application/json'
        )
        return response
    file = request.files['file']
    selected_model = request.form.get('model')
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        response = app.response_class(
            response=json.dumps({'message': 'No selected file'}),
            status=422,
            mimetype='application/json'
        )
        return response
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # get hog features
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        features = get_hog_features(image_path)

        result = ''
        if selected_model == 'knn':
            # load kNN the model from disk
            loaded_model = pickle.load(open('models/knnpickle_file', 'rb'))
            result = loaded_model.predict(features.flatten().reshape(1, -1))
        elif selected_model == 'dt':
            # load DT the model from disk
            loaded_model = pickle.load(open('models/dtickle_file', 'rb'))
            result = loaded_model.predict(features.flatten().reshape(1, -1))
        elif selected_model == 'nb':
            # load NV the model from disk
            loaded_model = pickle.load(open('models/gnbPickle_file', 'rb'))
            result = loaded_model.predict(features.flatten().reshape(1, -1))

        response = app.response_class(
            response=json.dumps({
                'message': 'This is endpoint',
                'model': selected_model,
                'result': label_decode(result[0])
            }),
            status=200,
            mimetype='application/json'
        )
        return response


if __name__ == '__main__':
    app.run(debug=True)
