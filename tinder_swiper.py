from flask import Flask, request
import os

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
@app.route('/matches', methods=['GET'])
def upload():
    print(request.files)
    return app.send_static_file('markup/matches.html')
    

def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()