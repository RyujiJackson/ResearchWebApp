from tensorflow.keras import models
from tensorflow.keras import Input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import matplotlib.cm as cm
import numpy as np
import requests
import os

#below this message is gradcam and prediction part
#use model locally
"""
model_name = 'inception_resnet_v2'
model=load_model("model/Incep_Resnet_V2.h5")
img_size = 384
"""

#donwload model from git release
model_name = 'inception_resnet_v2'
model_path = "model/Incep_Resnet_V2.h5"
model_url = "https://github.com/RyujiJackson/ResearchWebApp/releases/download/v.1.0.0/Incep_Resnet_V2.h5"  # Update with actual release URL
img_size = 384

# Download model if not present
def download_model():
    if not os.path.exists(model_path):
        print("Downloading model...")
        response = requests.get(model_url, stream=True)
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Model downloaded successfully.")

# Ensure model is downloaded
download_model()

# Load model
model = load_model(model_path)




def prediction(img):
	processed_img = img_preprocesssing(img)
	pred = model.predict(processed_img)
	pred = pred[0][0]
	pred = '%.2f'%(pred*100)
	pred_class = model.predict_classes(processed_img)
	if pred_class == 1:
		result = "感染"
	else:
		result = "非感染"

	return pred,result

def gradcam(img):
	names = [l.name for l in model.layers]
	incep_names = [l.name for l in model.get_layer("inception_resnet_v2").layers]

	last_conv_layer = model.get_layer(model_name).get_layer(incep_names[-4])
	last_conv_layer_model = models.Model(model.get_layer(model_name).inputs, last_conv_layer.output)
	classifier_input = Input(shape=last_conv_layer.output.shape[1:])
	x = classifier_input

	x = model.get_layer(model_name).get_layer(incep_names[-3])(x)
	x = model.get_layer(model_name).get_layer(incep_names[-2])(x)
	x = model.get_layer(model_name).get_layer(incep_names[-1])(x)
	x = model.get_layer(names[-2])(x)
	x = model.get_layer(names[-1])(x)

	classifier_model = models.Model(classifier_input, x)

	img_array = img_preprocesssing(img)
	img = image.img_to_array(img)
	with tf.GradientTape() as tape:
        # Compute activations of the last conv layer and make the tape watch it
		last_conv_layer_output = last_conv_layer_model(img_array)
        # print(last_conv_layer_output)
		tape.watch(last_conv_layer_output)
        # Compute class predictions
		preds = classifier_model(last_conv_layer_output)
		top_pred_index = tf.argmax(preds[0])
		top_class_channel = preds[:, top_pred_index]

	grads = tape.gradient(top_class_channel, last_conv_layer_output)
	pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
	last_conv_layer_output = last_conv_layer_output[0]
	heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
	heatmap = tf.squeeze(heatmap)

	heatmap = np.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

	heatmap = np.uint8(255 * heatmap)
	jet = cm.get_cmap("gray")

    # We use RGB values of the colormap
	jet_colors = jet(np.arange(256))[:, :3]
	jet_heatmap = jet_colors[heatmap]
	jet_heatmap = image.array_to_img(jet_heatmap)
	jet_heatmap = jet_heatmap.resize((256,256))

	jet = cm.get_cmap("jet")

	jet_colors = jet(np.arange(256))[:, :3]
	jet_heatmap = jet_colors[heatmap]

	jet_heatmap = image.array_to_img(jet_heatmap)
	jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))

	jet_heatmap = image.img_to_array(jet_heatmap)

    # Superimpose the heatmap on original image
	superimposed_img = jet_heatmap * 0.4 + img
	superimposed_img = image.array_to_img(superimposed_img)
	return jet_heatmap

def img_preprocesssing(img):
	img = img.resize((img_size,img_size))
	img = image.img_to_array(img)
	img = img/255
	img = np.expand_dims(img, axis=0)
	return img