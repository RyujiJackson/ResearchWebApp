import os
import io
from app import app
from flask import Flask,flash,request,redirect,render_template,send_file
from werkzeug.utils import secure_filename
from keras.preprocessing import image
from prediction_grad import *
import shutil
from datetime import datetime

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','dcm'])

#below this message is web function part
#array to store filenames,pred and results
file_names = []
pred_list = []
result_list = []

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload_and_result.html')

@app.route('/', methods=['POST'])
def upload_image():
	#delete old files
	for f in os.listdir("static/uploads/origin/"):
		os.remove(os.path.join("static/uploads/origin/", f))
	for f in os.listdir("static/uploads/heatmap/"):
		os.remove(os.path.join("static/uploads/heatmap/", f))
	#clear array to prevent showing old image
	file_names.clear()

	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')

	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			img = image.load_img("static/uploads/origin/" + filename)
			pred,result = prediction(img)
			pred_list.append(pred)
			result_list.append(result)
			heatmap = gradcam(img)
			image.save_img("static/uploads/heatmap/" + filename,heatmap)
	return render_template('upload_and_result.html', filenames=file_names,prediction=pred_list,results=result_list)

#app route to redirect for file downloading
@app.route('/download_file')
def download_file():
	shutil.make_archive('result/heatmap', format='zip', root_dir='.', base_dir='static/uploads/heatmap')
	path = "result/heatmap.zip"
	return send_file(path, as_attachment=True)

#function to show detail of clicked image
@app.route('/diagnose/', methods=['POST'])
def diagnose():
	files = request.files.getlist('files[]')
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			img = image.load_img("static/uploads/origin/" + filename)
			pred,result = prediction(img)
			pred_list.append(pred)
			result_list.append(result)

	show_data = request.form['detail_of_case']
	img_index = request.form['img_index']
	data_to_show = True
	show_result = False

	return render_template('upload_and_result.html', filenames=file_names,prediction=pred_list,results=result_list,detail=show_data,data_to_show=data_to_show,show_result=show_result,img_index=int(img_index))

#function to show AI result of current image
@app.route('/diagnose/result', methods=['POST'])
def diagnose_result():
	files = request.files.getlist('files[]')
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			img = image.load_img("static/uploads/origin/" + filename)
			pred,result = prediction(img)
			pred_list.append(pred)
			result_list.append(result)

	show_data = request.form['detail_of_case']
	img_index = request.form['img_index']
	data_to_show = True
	show_result = True

	return render_template('upload_and_result.html', filenames=file_names,prediction=pred_list,results=result_list,detail=show_data,data_to_show=data_to_show,show_result=show_result,img_index=int(img_index))

if __name__ == "__main__":
    app.run()