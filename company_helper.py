from models import db, Company, Client


def addCompany(company_name):
    company = Company()

    company.company_name = company_name
    company.company_status = "trial"
    company.count_client = 10
    company.count_user = 2

    db.session.add(company)
    db.session.commit()

    return Company.query.filter(Company.company_name == company_name).first()

def getCompany(id):
    return Company.query.get(id)



def delCompany(company):
    db.session.delete(company)
    db.session.commit()

def change_tariff(company, count_user, count_client):
    company.count_client = count_client
    company.count_user = count_user
    db.session.commit()


