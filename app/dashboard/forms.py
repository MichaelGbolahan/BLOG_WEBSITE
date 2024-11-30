from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,PasswordField,TextAreaField,SelectField,FileField,SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class BlogPost(FlaskForm):
    title=StringField('Title',validators=[DataRequired()])
    content=CKEditorField('Content',validators=[DataRequired()])
    image=FileField('Image',validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Image only please!')])
    submit=SubmitField('Submit')

    def __init__(self,*args,**kwargs):
        super(BlogPost,self).__init__(*args,**kwargs)