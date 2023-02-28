from flask import render_template,redirect,url_for,request,Blueprint
from flask_login import current_user

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
        company = current_user.company
        possition = 'user'

        print(f"{login} - {password} - {company} - {possition}")

        addUser(login,password,company, possition)


        return redirect(url_for("user.list_user"))


    return render_template("/user/add_user.html")



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
