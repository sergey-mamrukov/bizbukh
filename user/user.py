from flask import render_template,redirect,url_for,request,Blueprint, flash
from flask_login import current_user

from secrets import token_hex

from user_helper import getUsersForCompany,getUser,addUser, getClientsForUser,delUser,delaccaunt,editUser,checkUser
from tariff_helper import check_count_user

user = Blueprint("user",__name__,template_folder="templates")

@user.route("/")
def list_user():

    users = getUsersForCompany(current_user.company)
    company = current_user.company
    count_users_in_company = len(getUsersForCompany(company))
    if current_user.possition != "admin":
        return redirect(url_for("user.list_user"))

    return render_template("user/list_user.html",users=users, company=company, count_users_in_company=count_users_in_company)


@user.route("/adduser", methods= ['POST','GET'])
def add_user():
    if current_user.possition != "admin":
        return redirect(url_for("user.list_user"))

    if not check_count_user(current_user.company):
        flash("Ошибка добавления пользователей! Перейдите на другой тариф.")
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
        elif not name:
            flash("Поле имя должно быть заполнено!")
        elif not surname:
            flash("Поле фамилия должно быть заполено")
        elif not (password and len(password) >= 8):
            flash("Пароль должен быть не менее 8 символов!")
        elif checkUser(login):
            flash("Пользовательс таким email уже существует в системе")
        else:
            addUser(login, password, company, possition, name, surname)
            return redirect(url_for("user.list_user"))


    return render_template("/user/add_user.html", pwd = token_hex(8))



@user.route("/<int:userid>")
def cart_user(userid):
    user = getUser(userid)
    clients = getClientsForUser(user)



    return render_template("user/cart_user.html",user = user, clients = clients)


@user.route("/edit/<int:userid>", methods = ['GET','POST'])
def edit_user(userid):
    user = getUser(userid)

    if current_user.possition != "admin":
        return redirect(url_for("user.list_user"))

    if request.method == 'POST':

        login = request.form.get("login")
        password = request.form.get("password")
        name = request.form.get("name")
        surname = request.form.get("surname")



        if not login:
            flash("Поле email должно быть заполнено!")
        if not name:
            flash("Поле имя должно быть заполнено!")
        elif not surname:
            flash("Поле фамилия должно быть заполено")
        elif not (password and len(password) >= 8):
            flash("Пароль должен быть не менее 8 символов!")
        elif checkUser(login) and user.login != login:
            flash("Пользовательс таким email уже существует в системе")
        else:
            editUser(user,login,password,name,surname)
            return redirect(url_for("user.list_user"))


    return render_template("user/edit_user.html",user=user)

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
