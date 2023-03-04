from models import db, User
from client_helper import get_all_clients, delClient
from company_helper import delCompany

def addUser(login, password, company, possition, name, surname):
    user = User()

    user.login = login
    user.password = password
    user.company = company
    user.possition = possition
    user.name = name
    user.surname = surname

    db.session.add(user)
    db.session.commit()


def editUser(user, login, password, name, surname):
    user.login = login
    user.password = password
    user.name = name
    user.surname = surname
    db.session.commit()




def checkUser(login):
    if User.query.filter(User.login == login).first():
        return True
    else: return  False

def delUser(user):
    db.session.delete(user)
    db.session.commit()

def getUser(id):
    return User.query.get(id)

def getUsersForCompany(company):
    users = User.query.filter(User.company == company).all()
    return users


def getClientsForUser(user):
    clients = get_all_clients()
    result = []
    for client in clients:
        if user in client.user:
            result.append(client)

    return result


def delaccaunt(company):
    users = getUsersForCompany(company)
    clients = get_all_clients()
    for client in clients:
        delClient(client)

    for user in users:
        delUser(User.query.get(user.id))

    delCompany(company)




    print("delaccaunt")






