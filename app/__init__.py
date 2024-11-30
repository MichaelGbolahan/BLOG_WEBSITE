from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
import os
from flask_msearch import Search

# Base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize Flask app
app = Flask(__name__)

# Initialize CKEditor
ckeditor = CKEditor(app)

# Load configuration
app.config.from_pyfile('config.cfg')
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/pictures')


# Upload configuration
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Initialize extensions
db = SQLAlchemy(app)  # SQLAlchemy is initialized first
bcrypt = Bcrypt(app)

search = Search(db=db)
search.init_app(app)  # Ensure `search.init_app` is called after `db` initialization

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'Please login first now now.'



# Import views and models
from app import views, models
from app.dashboard import views as dashboard_views
from app.dashboard import models as dashboard_models

# Cache buster filter
import hashlib

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

@app.template_filter('cache_buster')
def cache_buster(file_url):
    file_path = os.path.join(app.root_path, file_url.lstrip('/'))
    if os.path.exists(file_path):
        file_hash = get_file_hash(file_path)
        if '?' in file_url:
            return f"{file_url}&v={file_hash}"
        else:
            return f"{file_url}?v={file_hash}"
    return file_url  # Return the original URL if file does not exist

app.jinja_env.filters['cache_buster'] = cache_buster