from flask import Flask
from os import path

STATIC_FOLDER = 'static/'
IMAGES_FOLDER = 'images/'

app = Flask(__name__)
app._static_folder = STATIC_FOLDER

@app.route('/')
def root():
    return app.send_static_file('markup/tinder_swiper.html')

# Respond with token that the user can use to acess a preview of the profiles in real time
#   Token is a hash of the image sent (sha1? murmur2?)
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and '.' in file.filename:
        # Create a hash and save it
        filename = str(hash(file) + file.filename.rsplit('.', 1)[1]
        file.save(IMAGES_FOLDER + filename)
    

if __name__ == "__main__":
    app.run()
