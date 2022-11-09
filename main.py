#import library

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, Login

app = Flask(__name__)



import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amani5759@",
    database="testdk"
)

mycur=mydb.cursor()

#mycur.execute("CREATE TABLE USER(email VARCHAR(100),password VARCHAR(100),name VARCHAR(100),UNIQUE(email))")


sqlformula="INSERT INTO USER (email,name,password) VALUES (%s,%s,%s)"

mydb.commit()






app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


##CONNECT TO DB

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



@app.route('/')
def get_all_posts():
    #osts = BlogPost.query.all()
    return render_template("index.html")

# Create the User Table
class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

# Create all the tables in the database
db.create_all()
# Register new users into the User database
@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(form.Password.data)
        new_user = User(email=form.Email.data, name=form.Name.data, password=hash_and_salted_password)

        datasql=(form.Email.data,form.Name.data,hash_and_salted_password)
        mycur.execute(sqlformula,datasql)
        mydb.commit()

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route('/login_successful',methods=["GET", "POST"])
def login_successful():
    return render_template("loh.hyml.html",)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = Login()
    if form.validate_on_submit():
        email = form.Email.data
        password = form.Password.data
        user = User.query.filter_by(email=email).first()



        # Email doesn't exist
        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('login_successful'))
    return render_template("login.html", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return render_template("Lout.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(port=5500, debug=True)