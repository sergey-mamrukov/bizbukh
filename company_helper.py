from models import db, Company, Client


def addCompany(company_name):
    company = Company()

    company.company_name = company_name

    db.session.add(company)
    db.session.commit()

    return Company.query.filter(Company.company_name == company_name).first()

def getCompany(id):
    return Company.query.get(id)

def getClientsForCompany(company):
    clients = Client.query.filter(Client.company == company).all()
    return clients

def delCompany(company):
    db.session.delete(company)
    db.session.commit()


