from . import db
from flask_login import UserMixin

class User(db.Model , UserMixin):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)
    blog_posts = db.relationship('BlogPost', backref='user', lazy=True)
    comment = db.relationship('Comment', backref='user', lazy=True)
    
class Blogpost(db.Model):
    __tablename__ = 'blogpost'
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50))
    author=db.Column(db.String(50))
    content=db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    
class Comment(db.Model):
    __tablename__ = 'comment'
    id=db.Column(db.Integer, primary_key=True)
    comment=db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    blogpost_id=db.Column(db.Integer,db.ForeignKey('blogpost.id'))
    
    