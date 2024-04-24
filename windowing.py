import pydicom
import numpy as np
import matplotlib.pyplot as plt

def show_dicom_image(dicom_file, window_level=None, window_width=None):
  """
  This function reads a DICOM image, applies windowing (optional), and displays it using Matplotlib.

  Args:
      dicom_file (str): Path to the DICOM file.
      window_center (int, optional): Window center value (default: None, uses data range).
      window_width (int, optional): Window width value (default: None, uses data range).
  """

  dataset = pydicom.dcmread(dicom_file)

  # Get image data
  image_data = dataset.pixel_array.astype(float)
  

  # Check if slope and intercept are available
  if 'RescaleSlope' in dataset and 'RescaleIntercept' in dataset:
    slope = dataset.RescaleSlope
    intercept = dataset.RescaleIntercept
  else:
    slope = 1
    intercept = 0
    print("Warning: Using default slope (1) and intercept (0) for rescaling.")

  # Rescale image data
  image_data = (image_data * slope) + intercept
  

  fig = plt.figure()
  # Display image using Matplotlib
  fig.add_subplot(221)
  plt.imshow(image_data, cmap='gray')
  plt.title(f"{dicom_file} - DICOM Image")
  plt.colorbar()
  plt.axis('off')




  # Apply windowing (if provided)
  if window_level and window_width:
    min_window = window_level - (window_width / 2)
    max_window = window_level + (window_width / 2)
    image_data[image_data < min_window] = min_window
    image_data[image_data > max_window] = max_window
    image_data = np.clip(image_data, min_window, max_window)

  fig.add_subplot(222)
  plt.imshow(image_data, cmap='gray')
  plt.title(f"{dicom_file} - DICOM Image")
  plt.colorbar()
  plt.axis('off')

  plt.show()
"""

  # Display image using Matplotlib
  fig.add_subplot(222)
  plt.title('histogram ')
  plt.hist(image_data)

  # Display image using Matplotlib
  fig.add_subplot(224)
  plt.title('histogram ')
  plt.hist(image_data)
"""



# Example usage
dicom_path = "static/uploads/DICOM/20150414000010001.DCM"

# With windowing (adjust values for your modality)
window_level = 3000
window_width = 2000

show_dicom_image(dicom_path, window_level, window_width)