from flask import Flask, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
from hashlib import sha256

template_dir = os.path.join(os.path.dirname(__file__), 'templates' )
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer,nullable=False, default=0) 
    

    def __repr__(self):
    	return '<User %r>' % self.username

	
	
def render_str(template,**params):
   t = jinja_env.get_template(template)
   return t.render(params)

def render(template, **kw):
   return render_str(template, **kw)

   
   
@app.route("/register" , methods=['GET', 'POST'])
def register ():
	if request.method == 'GET':
		return render("register.html")
	if request.method == "POST":
		name = request.form['login']
		password = request.form['password']
		user = User(username=name, password = sha256(password.encode('utf-8')).hexdigest())
		db.session.add(user)
		db.session.commit()
		return "<h1> ZAGADKU CUDA 2 </h1>"
		
		
		
@app.route("/")
def hello():
    return "FILE HTML PLS"
app.secret_key = 'VERY VERY SECRET KEEEY'


if __name__ == '__main__':
	app.run(debug = True)