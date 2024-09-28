from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import model_inference 
import os

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions (you can modify this as needed)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the file is an allowed type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']

        # If no file is selected
        if file.filename == '':
            return "No selected file"
        
        # If file is valid and allowed
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)  # Save the file to the upload folder
            
            # Model Prediction
            maximum_probability,predicted_class,graph_path = model_inference.predict(file_path)

            # Render the uploaded image in the template
            return render_template('index.html', filename=filename, maximum_probability = maximum_probability,predicted_class= predicted_class)

    return render_template('index.html')

# Route to display the uploaded image
@app.route('/uploads/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'))
    
# Route to display the graph image
@app.route('/graphs/<filename>')
def graph_image(filename):
    return redirect(url_for('static', filename=f'graphs/{filename}'))

if __name__ == "__main__":
    app.run(debug=True)
