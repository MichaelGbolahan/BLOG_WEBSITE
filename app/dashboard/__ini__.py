from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_migrate import Migrate
from flask_ckeditor import CKEditor


basedir = os.path.abspath(os.path.dirname(__file__))
app=Flask(__name__)
ckeditor=CKEditor(app)
app.config.from_pyfile('config.cfg')
app.config.from_pyfile('config.cfg')
app.config.from_pyfile('config.cfg')
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/pictures')

photos=UploadSet('photos',IMAGES)
configure_uploads(app,photos)
patch_request_class(app)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = u'please login first now'




db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app,db)



from app import views,models

from app.dashboard  import views