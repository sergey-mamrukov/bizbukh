from models import db, Tag


# получить тэг по id
def get_tag(id):
    return  Tag.query.get(id)

# получить все тэги
def get_all_tag():
    return Tag.query.all()