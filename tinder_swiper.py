from flask import Flask, render_template
import os
import glob
import pandas as pd
import numpy as np


STATIC_FOLDER = 'static'
IMAGES_FOLDER = 'images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app._static_folder = STATIC_FOLDER

@app.route('/')
def root():
    return app.send_static_file('markup/tinder_swiper.html')

# Respond with token that the user can use to acess a preview of the profiles in real time
#   Token is a hash of the image sent (sha1? murmur2?)
@app.route('/upload', methods=['POST'])
def upload():
    print(request.files)


def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compare(base_fp: str, comparison_fp: str) -> float:
    """ Returns the distance between base and comparison. Returns 
        lowest distance if there are multiple faces.
        Base and comparison are filepaths to CSVs.
    """
    base_arr = pd.read_csv(base_fp).loc[:, ' x_0':' y_67'].values
    comparison_arr = pd.read_csv(comparison_fp).loc[:, ' x_0':' y_67'].values
    
    if comparison_arr.shape[0] == 1:
        return np.sqrt(np.sum((base_arr - comparison_arr) ** 2) / base_arr.shape[1])
    
    elif comparison_arr.shape[0] > 1:
        dist = float('inf')
        
        for row in comparison_arr:
            d = np.sqrt(np.sum((base_arr - row) ** 2) / base_arr.shape[1])
            if d < dist: dist = d
            
        return dist
    
    else:
        return -1
    
def batch_compare(base_fp: str, comparison_dir: str) -> float:
    base_arr = pd.read_csv(base_fp).loc[:, ' x_0':' y_67'].values
    results = {}
    
    for comparison_csv in glob.glob(comparison_dir):
        #results[]
        pass

if __name__ == "__main__":
    app.run()