from app import db
from datetime import datetime

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)



    def __repr__(self):
        return '<name %r>' % self.name


class Post(db.Model):
    __searchable__=['title','content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey('category.id'),nullable=False)
    category=db.relationship('Category',backref='category',lazy=True)
    image = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User',backref='author',lazy=True)
    date_posted = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)

    def __repr__(self):
        return '<title %r>' % self.title