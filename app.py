import os
from flask import Flask, render_template, request, jsonify
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

def get_common_colors(image_path, num_colors=5):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        
        # Convert the image data to a numpy array
        img_array = np.array(img)
        
        # Reshape the array to a list of pixels
        pixels = img_array.reshape((-1, 3))
        
        # Use KMeans clustering to find dominant colors
        kmeans = KMeans(n_clusters=num_colors)
        kmeans.fit(pixels)
        
        # Get the RGB values of the cluster centers (dominant colors)
        dominant_colors = kmeans.cluster_centers_.astype(int)
        
        return dominant_colors.tolist()
    
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
                uploaded_file.save(image_path)
                most_common_colors = get_common_colors(image_path)
                return jsonify(most_common_colors)
            except Exception as e:
                return jsonify({"error": str(e)})
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
