import os
import io
from app import app
from flask import Flask,flash,request,redirect,render_template,send_file,jsonify
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

def empty_directory(directory_path):

  # Check if directory exists
  if not os.path.exists(directory_path):
    raise OSError(f"Directory '{directory_path}' does not exist.")

  # Iterate over directory contents (excluding '.' and '..')
  for filename in os.listdir(directory_path):
    if filename in ('.', '..'):
      continue  # Skip special directories
    full_path = os.path.join(directory_path, filename)
    if os.path.isfile(full_path):
      try:
        os.remove(full_path)
        # Optional: print(f"Deleted file: {full_path}")
      except OSError as e:
        print(f"Error deleting file '{full_path}': {e}")
    elif os.path.isdir(full_path):
      try:
        shutil.rmtree(full_path, ignore_errors=True)  # Ignore errors for empty subdirs
        # Optional: print(f"Deleted directory: {full_path}")
      except OSError as e:
        print(f"Error deleting directory '{full_path}': {e}")


def clear_data():
	for folder in ["origin", "heatmap"]:
		for f in os.listdir(f"static/uploads/{folder}"):
			os.remove(os.path.join(f"static/uploads/{folder}", f))
	
	empty_directory("static/annotation")
	file_names.clear()
	pred_list.clear()
	result_list.clear()

@app.route('/')
def home():
	return render_template('upload_and_result.html')

@app.route('/', methods=['POST'])
def upload_image():
	clear_data()

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
	img_index = request.form['to_get_img_index']
	data_to_show = True
	show_result = False

	return render_template('upload_and_result.html', filenames=file_names,prediction=pred_list,results=result_list,data_to_show=data_to_show,show_result=show_result,img_index=int(img_index))

#function to show AI result of current image
@app.route('/diagnose/result', methods=['POST'])
def diagnose_result():
	img_index = request.form['img_index']
	data_to_show = True
	show_result = True

	return render_template('upload_and_result.html', filenames=file_names,prediction=pred_list,results=result_list,data_to_show=data_to_show,show_result=show_result,img_index=int(img_index))

@app.route("/save_array", methods=["POST"])
def save_array():
	# Get data from request
	data = request.get_json()
	# Check if data is valid JSON
	if not data:
		return jsonify({"error": "Invalid JSON data"}), 400
	# Extract array and imgIndex (assuming the key is 'array')
	array_data = data["array"]
    #times coordinates by 2 to be the same as original image size
    #array_data = [float(element) * 2 for element in array_data if str(element).isdigit()]
	print(array_data)
	img_index = data["imgIndex"]
	print(img_index)
  
	directory = os.path.join("static/annotation/", img_index)

	if not os.path.exists(directory):
		os.mkdir(directory)
	
   	# Check if "array.txt" exists
	if os.path.exists(os.path.join(directory,"array.txt")):
		os.remove(os.path.join(directory,"array.txt"))
	
	try:
		with open(os.path.join(directory,"array.txt"), "w") as f:
			f.write(str(array_data))
		return jsonify({"message": "Array saved successfully!"}), 201
	except Exception as e:
		return jsonify({"error": f"Saving array failed: {e}"}), 500

if __name__ == "__main__":
    app.run()