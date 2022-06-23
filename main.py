import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from svd_compressor import *
from jpeg_compressor import *

app = Flask(__name__, template_folder='templates')
app.secret_key = "super secret key"
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PROCESSED_FOLDER = 'static/processed'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
def getFile_extension(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower()

@app.route('/')
def upload_form():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def getIMG():
	if not os.path.isdir(app.config['UPLOAD_FOLDER']):
		os.mkdir(app.config['UPLOAD_FOLDER'])
	else:
		files = os.listdir(app.config['UPLOAD_FOLDER'])
		for item in files:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item))

	files = os.listdir(app.config['UPLOAD_FOLDER'])
	if len(files) > 0:
		for item in files:
			os.remove(os.path.join(app.config['UPLOAD_FOLDER'], item))

	if request.method == 'POST':
		img = request.files['file']
		# print(request.form['method'])
		img.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(img.filename)))
	if request.form['method'] == 'svd':
		return svd__compressor()
	elif request.form['method'] == 'jpeg':
		return jpeg__compressor()

@app.route('/getslider', methods=['GET', 'POST'])
def get_slider():
	data = request.data
	k = int(data)
	print(k)
	return k

@app.route('/svd_compressor', methods=['GET', 'POST'])
def svd__compressor():
	img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'] ,os.listdir(app.config['UPLOAD_FOLDER'])[0]))
	input_image = np.asarray(img)
	try:
		compress = svd_compress(input_image, k=get_slider())
	except:
		compress = svd_compress(input_image, k=0)
		
	ext = getFile_extension(os.path.join(app.config['UPLOAD_FOLDER'] ,os.listdir(app.config['UPLOAD_FOLDER'])[0]))
	if not os.path.isdir(PROCESSED_FOLDER):
		os.mkdir(PROCESSED_FOLDER)
	else:
		files = os.listdir(PROCESSED_FOLDER)
		for item in files:
			os.remove(os.path.join(PROCESSED_FOLDER, item))
			
	compress.save(os.path.join(PROCESSED_FOLDER, f'result.{ext}'))
	response = {
                "data": [os.path.join(PROCESSED_FOLDER, f'result.{ext}'), img.size[0], img.size[1], compress.size[0] * compress.size[1]]
            } # [img, w, h, number_of_pixel compressed img]
	return jsonify(response), 200

@app.route('/jpeg_compressor', methods=['GET', 'POST'])
def jpeg__compressor():
	image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'] ,os.listdir(app.config['UPLOAD_FOLDER'])[0]))

	ext = getFile_extension(os.path.join(app.config['UPLOAD_FOLDER'] ,os.listdir(app.config['UPLOAD_FOLDER'])[0]))
	if not os.path.isdir(PROCESSED_FOLDER):
		os.mkdir(PROCESSED_FOLDER)
	else:
		files = os.listdir(PROCESSED_FOLDER)
		for item in files:
			os.remove(os.path.join(PROCESSED_FOLDER, item))
	
	try:
		compress = jpeg_compress(image, quality=get_slider())
	except:
		compress = jpeg_compress(image, quality=50)
	compress = cv2.cvtColor(compress, cv2.COLOR_RGB2BGR)
	cv2.imwrite(os.path.join(PROCESSED_FOLDER, f'result.{ext}'), compress)
	response = {
                "data": [os.path.join(PROCESSED_FOLDER, f'result.{ext}'), image.shape[1], image.shape[0], compress.shape[0] * compress.shape[1]]
            } # [img, w, h, number_of_pixel compressed img]
	return jsonify(response), 200

if __name__ == "__main__":
    app.debug = True
    app.run(port='8000')