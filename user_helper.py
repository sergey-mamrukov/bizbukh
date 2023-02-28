from models import db, User, Company, Client
from flask_login import current_user
from client_helper import get_all_clients, delClient
from company_helper import delCompany

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






