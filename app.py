from flask import Flask
from flask_bootstrap import Bootstrap

UPLOAD_FOLDER = 'static/uploads/origin/'

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024