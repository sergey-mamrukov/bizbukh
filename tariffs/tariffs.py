from flask import Flask, Blueprint, render_template,url_for,flash,redirect
from flask_login import current_user

from tariff_helper import change_tariff, switch_tariff
from client_helper import getClientsForCompany
from user_helper import getUsersForCompany


tariffs = Blueprint('tariffs', __name__, template_folder='templates')

@tariffs.route('/')
def selecttariff():
    return render_template("tariffs/tariffs.html")

@tariffs.route('/applytariff/<int:tariffnumber>')
def applytariff(tariffnumber):
    company = current_user.company
    # count_user = company.count_user
    # count_client = company.count_client
    count_clients_in_company = len(getClientsForCompany(company))
    count_users_in_company = len(getUsersForCompany(company))

    if tariffnumber == 1:
        if switch_tariff(count_users_in_company,count_clients_in_company,1,15):
        # if switch_tariff(2,16, 1, 15):
            change_tariff(company,1,15)
            flash("Тариф успешно применен", "success")
        else:
            flash("Тариф невозможно применить! Количество клиентов или пользователей превышает предусмотренное тарифом",
                  "error")

    if tariffnumber == 2:
        if switch_tariff(count_users_in_company, count_clients_in_company, 5, 55):
            change_tariff(company,5,55)
            flash("Тариф успешно применен", "success")
        else: flash("Тариф невозможно применить! Количество клиентов или пользователей превышает предусмотренное тарифом",
                    "error")

    if tariffnumber == 3:
        if switch_tariff(count_users_in_company, count_clients_in_company, 25, 155):
            change_tariff(company, 25, 155)
            flash("Тариф успешно применен", "success")
        else:
            flash("Тариф невозможно применить! Количество клиентов или пользователей превышает предусмотренное тарифом",
                  "error")

    if tariffnumber == 4:
        if switch_tariff(count_users_in_company, count_clients_in_company, 100, 300):
                change_tariff(company, 100, 300)
                flash("Тариф успешно применен", "success")
        else:
            flash("Тариф невозможно применить! Количество клиентов или пользователей превышает предусмотренное тарифом",
                  "error")

    return redirect(url_for("tariffs.selecttariff"))