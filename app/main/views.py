from . import app
from flask import request,jsonify,make_response
from werkzeug.security import generate_password_hash,check_password_hash
from ..models import User,Blogpost,Comment
import uuid
from .. import db

@app.route('/user', methods=['GET'])
def get_user():
    users = User.query.all()
    output = []
    
    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)
    return jsonify ({'users': output}) 
    
@app.route('/user/<public_id>', methods=['GET'])
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    
    if not user:
        return jsonify({'message': 'No user found!'})
    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name']= user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin
    
    
    return jsonify({'user' : user_data })
    
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
        
    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['DELETE'])
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()
    if not user:
        return jsonify({'message': 'No user found!'})
    user.admin = True
    db.session.commit()
    
    return jsonify({'message':'The user has been deleted!'})

#login

@app.route('/login')     
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401,{'WWW-Authenticate' : 'Basic realm = "Login required!"'})

    user = User.query.filter_by(name = auth.username).first()  

    if not user:
        return jsonify({'message' : 'user not found!'})    
    if check_password_hash(user.password , auth.password): 
        return jsonify ({'message' : 'Login successful!'})
    return jsonify({'message' : 'wrong password!'}) 

#blogpost
@app.route('/blogpost', methods=['GET'])
def get_blogpost():
    blogposts = Blogpost.query.all()
    output = []
    
    for blogpost in blogposts:
        blogpost_data = {}
        blogpost_data['id'] = blogpost.id
        blogpost_data['title'] = blogpost.title
        blogpost_data['author'] = blogpost.author
        blogpost_data['content'] = blogpost.content
        blogpost_data['user_id'] = blogpost.user_id
        output.append(blogpost_data)
    return jsonify ({'blogposts': output}) 
    
@app.route('/blogpost/<int:id>', methods=['GET'])
def get_one_blogpost(id):
    blogpost = Blogpost.query.filter_by(id=id).first()
    
    if not blogpost:
        return jsonify({'message': 'No blogpost found!'})
    blogpost_data = {}
    blogpost_data['id'] = blogpost.id
    blogpost_data['title']= blogpost.title
    blogpost_data['author'] = blogpost.author
    blogpost_data['content'] = blogpost.content
    blogpost_data['user_id'] = blogpost.user_id
    
    
    return jsonify({'blogpost' : blogpost_data })

@app.route('/blogpost', methods=['POST'])
def create_blogpost():
    data = request.get_json()
    new_blogpost = Blogpost(title=data['title'],user_id=data['user_id'] ,author=data['author'],content=data['content'])
    db.session.add(new_blogpost)
    db.session.commit()
        
    return jsonify({'message' : 'New blogpost created!'})

@app.route('/blogpost/<int:id>', methods=['DELETE'])
def delete_blogpost(id):
    blogpost = Blogpost.query.filter_by(id=id).first()
    if not blogpost:
        return jsonify({'message': 'No blogpost found!'})
    db.session.delete(blogpost)
    db.session.commit()
    
    return jsonify({'message':'The blogpost has been deleted!'})



@app.route('/comment' , methods = ['GET'])
def get_comment():
    comments = Comment.query.all()
    output = []
    
    for comment in comments:
        comment_data = {}
        comment_data['id'] = comment.id
        comment_data['comment'] = comment.comment
        comment_data['user_id'] = comment.user_id
        comment_data['blogpost_id'] = comment.blogpost_id
        output.append(comment_data)
    return jsonify ({'comments': output})

@app.route('/comment/<int:post_id>' , methods = ['GET'])
def get_blog_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    output = []
    
    for comment in comments:
        comment_data = {}
        comment_data['id'] = comment.id
        comment_data['comment'] = comment.comment
        comment_data['user_id'] = comment.user_id
        comment_data['post_id'] = comment.post_id
        output.append(comment_data)
    return jsonify ({'comments': output})





@app.route('/user/<public_id>/blogpost/comment' , methods = ['POST'])
def create_comment(public_id):
    user = User.query.filter_by(public_id = public_id).first()
    if user:
        data = request.get_json()
        new_comment = Comment(comment=data['comment'],user_id=data['user_id'],post_id=data['post_id'])
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({'message' : 'New comment created!'})
    return jsonify({'message' : 'No user found!'})

    

    
    
    