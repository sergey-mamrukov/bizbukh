from company_helper import change_tariff
from user_helper import getUsersForCompany
from client_helper import getClientsForCompany

def apply_tariff(company, count_user, count_client):
    change_tariff(company,count_user,count_client)

# Возвращает тру если количество зарегистрированных клиентов меньше количества разрешенных
def check_count_client(company):
    countclients = getClientsForCompany(company)
    if len(countclients) < company.count_client:
        return True
    else: return False

# Возвращает тру если количество зарегистрированных пользователей меньше количества разрешенных
def check_count_user(company):
    countusers = getUsersForCompany(company)
    if len(countusers) < company.count_user:
        return True
    else: return False


# Возвращает тру если переход на тариф ниже разрешен (количество пользователей и клиентов меньше или равно количеству в тарифе)
def switch_tariff(count_registred_user, count_registred_client, count_tariff_user, count_tariff_client):
    if count_tariff_user >= count_registred_user and count_tariff_client >= count_registred_client:
        return True
    else: return False
