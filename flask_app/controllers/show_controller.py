from flask_app import app
from flask import render_template,request,redirect,session
from flask_app.models.show import Show
from flask_app.models.user import User


@app.route("/create_show", methods = ["POST"])
def create_recipe():
    return redirect("/new")

@app.route("/new")
def new_show():
    if session['login'] == False:
        return redirect("/")
    return render_template("show.html")

@app.route("/save_show", methods=["POST"])
def save_show():
    if session['login'] == False:
        return redirect("/")

    if not Show.validate_show(request.form):
        return redirect('/new')

    data = {
        "title" :request.form["title"],
        "network" :request.form["network"],
        "release_date" :request.form["release_date"],
        "description" : request.form["description"],
        "user_id" : session["user_id"]
    }
    show_id = Show.save_show(data)
    return redirect("/dashboard")

@app.route("/show/<int:show_id>")
def show_info(show_id):
    if session['login'] == False:
        return redirect("/")
    data = {
        "id" : show_id
    }
    print(data)
    num_like = Show.num_like(data)
    show = Show.one_show(data)
    data2 = {
        "id":session['user_id']
    }
    user = User.one_user(data2)

    return render_template("show_info.html",show = show, user= user, num_like = num_like)

@app.route("/edit/<int:show_id>")
def edit_show(show_id):
    if session['login'] == False:
        return redirect("/")
    data = {
        "id" : show_id
    }
    show = Show.one_show(data)
    return render_template("edit_show.html",show = show)

@app.route("/update_show", methods = ["POST"])
def update_show():
    if session['login'] == False:
        return redirect("/")
    if not Show.validate_show(request.form):
        return redirect(f"/edit/{request.form['show_id']}")
    data = {
        "id": request.form["show_id"],
        "title" :request.form["title"],
        "network" :request.form["network"],
        "release_date" :request.form["release_date"],
        "description" : request.form["description"],
    }
    Show.update(data)
    return redirect("/dashboard")

@app.route('/delete/<int:show_id>')
def delete_show(show_id):
    data = {
        "id":show_id
    }
    Show.delete(data)
    return redirect('/dashboard')

@app.route("/like/<int:show_id>")
def like(show_id):

    data = {
        "show_id" : show_id ,
        "user_id":session['user_id']
    }
    # show = Show.one_show(data)
    Show.add_like(data)
    return redirect('/dashboard')
