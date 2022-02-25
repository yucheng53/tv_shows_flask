from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if not User.validate_user(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" :request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    session["login"] = True
    return redirect("/dashboard")

@app.route("/dashboard")
def welcome_user():
    if session['login'] == False:
        return redirect("/")

    data = {
        "id":session['user_id']
    }
    user = User.one_user(data)
    shows = Show.get_all_shows(data)
    return render_template('dashboard.html',user=user, shows = shows)

@app.route("/login", methods=["POST"])
def login():
    data = { "email" : request.form["email2"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password2']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['login'] = True
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop("user_id")
    session['login'] = False
    return redirect("/")
