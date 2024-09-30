# Importing Libraries
from tensorflow import keras
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
import warnings
import os

# Ignore warnings
warnings.filterwarnings("ignore")

# Ensure Matplotlib is using 'Agg' backend to avoid macOS GUI errors
import matplotlib
matplotlib.use('Agg')  # This disables GUI rendering on macOS

# Optional: Disable GPU usage if not needed
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

# Load the model with the best validation accuracy
loaded_best_model = keras.models.load_model("./model_07-0.78.h5")

# Custom function to load and predict label for the image
def predict(img_rel_path):
    # Load the image and resize to 256x256
    img = image.load_img(img_rel_path, target_size=(256, 256))
    
    # Convert Image to a numpy array
    img = image.img_to_array(img, dtype=np.uint8)
    
    # Scale the Image Array values between 0 and 1
    img = np.array(img) / 255.0
    
    # Get the Predicted Label for the loaded Image
    p = loaded_best_model.predict(img[np.newaxis, ...])
    
    # Label array
    labels = {0: 'Lumpy Skin', 1: 'Normal Skin'}
    
    # Find the maximum probability and predicted class
    maximum_probability = np.max(p[0], axis=-1)
    predicted_class = labels[np.argmax(p[0], axis=-1)]
    
    # Prepare data for the bar plot
    classes = []
    prob = []
    
    for i, j in enumerate(p[0], 0):
        print(labels[i].upper(), ':', round(j * 100, 2), '%')
        classes.append(labels[i])
        prob.append(round(j * 100, 2))
    
    # Function to generate the probability bar plot
    def plot_bar_x():
        # This is for plotting purpose
        index = np.arange(len(classes))
        plt.bar(index, prob)
        plt.xlabel('Labels', fontsize=8)
        plt.ylabel('Probability', fontsize=8)
        plt.xticks(index, classes, fontsize=8, rotation=20)
        plt.title('Probability for loaded image')
        
        # Save the plot as an image
        file_path = f"./static/graphs/{os.path.basename(img_rel_path)}"
        plt.savefig(file_path)
        plt.close()  # Make sure to close the plot to avoid resource leaks
        
        return file_path
    
    # Generate and return the plot file path along with the predictions
    file_path = plot_bar_x()
    return (maximum_probability, predicted_class, file_path)
