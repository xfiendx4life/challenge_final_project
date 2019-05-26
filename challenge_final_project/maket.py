from flask import Flask, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
import jinja2
from hashlib import sha256
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
db = SQLAlchemy(app)

template_dir = os.path.join(os.path.dirname(__file__), 'styles' )
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer,nullable=False, default=1) 
   

    def __repr__(self):
    	return '<User %r>' % self.username

	
	
def render_str(template,**params):
   t = jinja_env.get_template(template)
   return t.render(params)

def render(template, **kw):
   return render_str(template, **kw)

def check_user(name, password):
	user = User.query.filter_by(username = name).first()
	if user:
		return sha256(password.encode('utf-8')).hexdigest() == user.password
	else:
		return False   
   
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
		return redirect(url_for('quiz2'))

@app.route("/login" , methods=['GET', 'POST'])
def login ():
	if request.method == 'GET':
		return render("login.html")
	if request.method == "POST":
		name = request.form['login']
		password = request.form['password']
		user = User(username=name, password = sha256(password.encode('utf-8')).hexdigest())
		if check_user(name,password):
			session['name']=name
			session['password']=password
			return redirect(url_for('main'))
		else:
			return render("login.html")

@app.route("/" , methods=['GET', 'POST'])		
def hello():
    if request.method == 'POST':
        answer = request.form['answer1']
        if answer == 'C3PO':
            return redirect(url_for('register'))
    return render('1 quiz.html')


@app.route("/main" , methods=['GET', 'POST'])		
def main():
	name1=request.form['login']
	return render('main.html',imya = name1)

   	
@app.route("/quiz2" , methods=['GET', 'POST'])
def quiz2():
 return render('2 quiz.html')


app.secret_key = '5eca6d48fe37591126bbfcd1da97ba2e3b1d096a7dfecbfa7c390e80c5994a79'
if __name__ == '__main__':
 app.run(debug = True)