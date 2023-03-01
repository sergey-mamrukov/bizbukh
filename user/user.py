from flask import render_template,redirect,url_for,request,Blueprint, flash
from flask_login import current_user

from secrets import token_hex

from user_helper import getUsersForCompany,getUser,addUser, getClientsForUser,delUser,delaccaunt

user = Blueprint("user",__name__,template_folder="templates")

@user.route("/")
def list_user():

    users = getUsersForCompany(current_user.company)
    # print(users)
    if current_user.possition != "admin":
        return redirect(url_for("user.list_user"))

    return render_template("user/list_user.html",users=users)


@user.route("/adduser", methods= ['POST','GET'])
def add_user():
    if current_user.possition != "admin":
        return redirect(url_for("user.list_user"))

    if request.method == 'POST':

        login = request.form.get("login")
        password = request.form.get("password")
        name = request.form.get("name")
        surname = request.form.get("surname")


        company = current_user.company
        possition = 'user'




        if not login:
            flash("Поле email должно быть заполнено!")
        if not name:
            flash("Поле фамилия должно быть заполнено!")
        elif not surname:
            flash("Поле фамилия должно быть заполено")
        elif not (password and len(password) >= 8):
            flash("Пароль должен быть не менее 8 символов!")
        else:
            addUser(login, password, company, possition, name, surname)
            return redirect(url_for("user.list_user"))


    return render_template("/user/add_user.html", pwd = token_hex(8))



@user.route("/<int:userid>")
def cart_user(userid):
    user = getUser(userid)
    clients = getClientsForUser(user)



    return render_template("user/cart_user.html",user = user, clients = clients)


@user.route("/edit/<int:userid>")
def edit_user():
    return render_template("user/edit_user.html")

@user.route("/del/<int:userid>")
def del_user(userid):
    user = getUser(userid)

    delUser(user)
    return redirect(url_for("user.list_user"))




@user.route("/delaccaunt")
def del_accaunt():
    if current_user.possition == "admin":
        company = current_user.company
        delaccaunt(company)
        return redirect(url_for("login"))
    else: return redirect(url_for("login"))
