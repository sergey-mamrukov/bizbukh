from models import Event, Eventready, Eventstatus, Tag,Systnalog,Opf


# ----------------- Работа с моделью Event -----------------
# получить все события
def get_events():
    return Event.query.all()

# ----------------- Работа с моделью Tag -----------------
# получить все тэги
def get_all_tags():
    return Tag.query.all()


# ----------------- Работа с моделью Systnalog -----------------
# получить все системы налогообложения
def get_all_systnalog():
    return Systnalog.query.all()


# ----------------- Работа с моделью Opf -----------------
# получить все организационно-правовые формы
def get_all_opf():
    return Opf.query.all()

def get_opf(id):
    return  Opf.query.get(id)





# ----------------- Работа с моделью Eventready -----------------

# получить все выполненные события
def get_eventredy_all():
    return Eventready.query.all()

# получить все выполненные события
def get_eventredy_forclient(client):
    return Eventready.query.filter_by(client = client)




# ----------------- Работа с моделью Eventstatus -----------------
# получить все статусы
def get_eventstatuses():
    return Eventstatus.query.all()
