import os
from io import BytesIO

import pydicom.errors
from app import app
from flask import Flask,flash,request,redirect,render_template,send_file,jsonify
from werkzeug.utils import secure_filename
from keras.preprocessing import image
from prediction_grad import *
from windowing import *
import shutil
import pydicom  # For DICOM file handling
from PIL import Image  # For image conversion
import matplotlib.pyplot as plt
import urllib


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
	
	empty_directory("static/uploads/DICOM")
	empty_directory("static/annotation")
	file_names.clear()
	pred_list.clear()
	result_list.clear()

@app.route('/')
def home():
	return render_template('Diagnose.html')
#handle image upload
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
			
			# Check for DICOM format
			if filename.endswith('.DCM'):
				#convert dicom to png
				try:
					file.save(os.path.join('static/uploads/DICOM/', filename))
					# Read DICOM data using pydicom
					dataset = pydicom.dcmread(os.path.join('static/uploads/DICOM/', filename))
					
					#change file extension from dcm to png
					filename, _ = os.path.splitext(secure_filename(filename))  # Separate filename and extension
					filename = f"{filename}.png"

					arr = dataset.pixel_array.astype(float) # Pixel Data を ndarray に変換
					arr_normalized = (arr / arr.max())*255
					arr_normalized = np.uint8(arr_normalized) # float to int

					# Create a 3-channel image by replicating the grayscale data for all channels
					img = np.repeat(arr_normalized[..., None], 3, axis=2)  # Replicate for RGB

					#save processed Dicom image
					img = Image.fromarray(arr_normalized, mode="L")
					img = img.convert('RGB')  # Convert to RGB mode
					img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				except pydicom.errors.InvalidDicomError:
					flash(f"Error processing DICOM file: {filename}")
					continue
			else:
				#img = Image.open(file)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				img = image.load_img("static/uploads/origin/" + filename)
			
			#store edited filename into file_names array in case of uploaded DICOM file
			file_names.append(filename)

			pred,result = prediction(img)
			pred_list.append(pred)
			result_list.append(result)
			heatmap = gradcam(img)
			image.save_img("static/uploads/heatmap/" + filename,heatmap)
	return render_template('Diagnose.html', filenames=file_names,prediction=pred_list,results=result_list)

#app route to redirect for file downloading
@app.route('/download_file')
def download_file():
	shutil.make_archive('result/heatmap', format='zip', root_dir='.', base_dir='static/uploads/heatmap')
	path = "result/heatmap.zip"
	return send_file(path, as_attachment=True)

#function to show detail of clicked image
@app.route('/diagnose/', methods=['POST'])
def diagnose():
	img_index = request.form['detail_of_case']
	data_to_show = True
	show_result = False

	return render_template('Diagnose.html', filenames=file_names,prediction=pred_list,results=result_list,data_to_show=data_to_show,show_result=show_result,img_index=int(img_index))

#function to show AI result of current image
@app.route('/diagnose/result', methods=['POST'])
def diagnose_result():
	img_index = request.form['img_index']
	data_to_show = True
	show_result = True

	return render_template('Diagnose.html', filenames=file_names,prediction=pred_list,results=result_list,data_to_show=data_to_show,show_result=show_result,img_index=int(img_index))

@app.route("/update_image", methods=["POST"])
def update_image():
    window_level = int(request.form["window_level"])
    window_width = int(request.form["window_width"])
    filename_update = (request.form["filename"])
    #img_index = 0
    dicom_path = (os.path.join('static/uploads/DICOM/', filename_update))

    image_data = show_dicom_image(dicom_path, window_level, window_width)
    pil_image = Image.fromarray(image_data)
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    # Create an in-memory file-like object using BytesIO
    img_byte_arr = io.BytesIO()
    pil_image.save(img_byte_arr, format='PNG')  # Adjust format if needed
    img_data = urllib.parse.quote(img_byte_arr.getvalue())

    return img_data

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
	annotation_filename = data["annotation_filename"]
	print(annotation_filename)
  
	directory = os.path.join("static/annotation/", img_index)

	if not os.path.exists(directory):
		os.mkdir(directory)
	
   	# Check if "array.txt" exists
	if os.path.exists(os.path.join(directory,annotation_filename)):
		os.remove(os.path.join(directory,annotation_filename))
	
	try:
		with open(os.path.join(directory,annotation_filename), "w") as f:
			f.write(str(array_data))
		return jsonify({"message": "Array saved successfully!"}), 201
	except Exception as e:
		return jsonify({"error": f"Saving array failed: {e}"}), 500


if __name__ == "__main__":
    app.run()