from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://moringa:nancy@localhost/blogapp2'

db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    public_id=db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)
    
class Blogpost(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(50))
    author=db.Column(db.String(50))
    content=db.Column(db.String(255))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    
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



if __name__ == '__main__':
    app.run(debug=True)