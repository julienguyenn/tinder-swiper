from flask import Flask, request
from os import path, rename
from pathlib import Path
from openface_api.wrapper import process_pics

STATIC_FOLDER = 'static/'
BASE_FOLDER = 'base/'
PROCESSED_FOLDER = 'processed/'

app = Flask(__name__)
app._static_folder = STATIC_FOLDER

@app.route('/')
def root():
    return app.send_static_file('markup/tinder_swiper.html')

# Respond with token that the user can use to acess a preview of the profiles in real time
#   Token is a hash of the image sent (sha1? murmur2?)
@app.route('/matches', methods=['GET'])
def matches():
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
def match():
    token = request.args['token']
    if token:
        pass
        # Get profile and pictures from tinder api
        # Store pictures in /comparison/token/token{0-X}.jpg
        # Run open face in whole dir
        # Swipe right or left
        # Send best picture in comparison dir
        # For picture in comparison dir, delete picture and corresponding pic in processed
    

if __name__ == "__main__":
    app.run()
