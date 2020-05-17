'''
python -m pip install -U pip
python -m pip install -U flask python-dateutil wget
'''

from flask import Flask, request
import os
from os import path, rename
from pathlib import Path

import glob
import pandas as pd
import numpy as np

from openface_api.wrapper import process_pics
import glob
import pandas as pd
import numpy as np

import tinder_api.session

STATIC_FOLDER = 'static/'
BASE_FOLDER = 'base/'
PROCESSED_FOLDER = 'processed/'
COMPARISON_FOLDER = 'comparison/'

app = Flask(__name__)
app._static_folder = STATIC_FOLDER

sess = tinder_api.session.Session()

@app.route('/')
def root():
    return app.send_static_file('markup/tinder_swiper.html')

# Respond with token that the user can use to acess a preview of the profiles in real time
#   Token is a hash of the image sent (sha1? murmur2?)
@app.route('/matches', methods=['GET'])
def matches() -> None:
    file = request.files['file']
    if file and '.' in file.filename:
        # Create a hash and save it
        token = str(hash(file))
        filename = token + '.' + file.filename.rsplit('.', 1)[1]
        Path(BASE_FOLDER).mkdir(parents=True, exist_ok=True)
        filepath = BASE_FOLDER + filename
        file.save(filepath)

        # Create a base image
        process_pics(filepath)

        # Move the csv into base
        processed_file = PROCESSED_FOLDER + token + 'csv'
        os.rename(PROCESSED_FOLDER + processed_file, BASE_FOLDER + processed_file)
                
        return app.send_static_file('markup/matches.html')
    else:
        return 'Image not recieved', 400

@app.route('/api/match', methods=['GET'])
def match() -> None:
    token = request.args['token']
    if token:
        # Init session
        sess = session.Session()
        user_name = ""
        user_bio = ""
        
        # Download pictures to /comparison/token/token{0-X}
        for user in itertools.islice(sess.yield_users(), 1):
            download_image(user.photos, token, COMPARISON_FOLDER + str(token) + '/')
            
            user_name = user.name # store user name
            if user.bio is not "<MissingValue>":
                user_bio = user.bio # store user bio if not empty
            
        # Run open face in whole dir
        process_pics(in_dir='comparison/' + str(token) + '/')
        
        # Determine if similarity meets the threshold
        batch_compare(BASE_FOLDER + str(token) + '.csv', 'comparison/' + str(token))
        # Swipe right or left
        # Send best picture in comparison dir
        # For picture in comparison dir, delete picture and corresponding pic in processed


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
    
def batch_compare(base_fp: str, comparison_dir: str) -> tuple:
    """ Compare the base CSV to a directory containing comparison CSVs.
        Returns a tuple containing the (name of file and distance value).
        The tuple contains the comparison csv that is the most similar to base.
    """
    results = {}
    
    for comparison_csv in glob.glob(comparison_dir + '/*.csv'):
        filename = os.path.split(comparison_csv)[1].split('.')[0]
        results[filename] = compare(base_fp, comparison_csv)
        
    return (min(results, key=results.get), results[min(results, key=results.get)])

if __name__ == "__main__":
    pass
