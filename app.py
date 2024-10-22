from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
import gen_ai
import os
from flask_cors import CORS
import re


app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_filename(filename):
    pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'  # Matches lowercase alphanumeric and hyphens with no leading or trailing hyphens
    return bool(re.match(pattern, filename))

@app.route('/uploads', methods = ['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'no file in part request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'no file selected'})

    if file and allowed_file(file.filename):
        file_name = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        path = f'./uploads/{file_name}'
        resume = gen_ai.analise_tr(path)
        return resume

    else:
        return jsonify({'Erro': 'no analysis perfomed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

'''def index():
    if request.method == 'POST':
        data = request.get_json()
        path = data['path']
        resultado = main.analise_tr(path)
        return jsonify({'resultado' : resultado})
    if request.method == 'GET':
        return jsonify({'Parâmetros': main.list_criterios})
    else:
        return jsonify({'mensagem': 'método não permitido'})'''

