from . import db


def create_login():
    try:
        db.create_all()
        db.session.commit()
    except Exception as e:
        return "table not created"
