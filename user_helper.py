from models import db, User


def addUser(login, password, company, possition):
    user = User()

    user.login = login
    user.password = password
    user.company = company
    user.possition = possition

    db.session.add(user)
    db.session.commit()

def delUser(user):
    db.session.delete(user)
    db.session.commit()

def getUser(id):
    return User.query.get(id)

def getUsersForCompany(company):
    users = User.query.filter(User.company == company).all()
    return users


