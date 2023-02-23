from flask import Flask,render_template,url_for, Blueprint
from company_helper import getClientsForCompany

from flask_login import current_user

company = Blueprint('company', __name__, template_folder='templates')

@company.route("/")
def companyPage():
    clients = getClientsForCompany(current_user.company.id)
    print(clients)
    return render_template("company/company_page.html", clients = clients)