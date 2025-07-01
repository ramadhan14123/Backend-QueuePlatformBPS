from app.extensions import db
from app.models.visit import Visit
from datetime import datetime

def assign_queue_number():
    today = datetime.utcnow().date()
    last = db.session.query(db.func.max(Visit.queue_number))\
        .filter(db.func.date(Visit.timestamp) == today).scalar()
    return (last or 0) + 1

def reset_queue_number():
    today = datetime.utcnow().date()
    db.session.query(Visit).filter(db.func.date(Visit.timestamp) == today)\
        .update({Visit.queue_number: None})
    db.session.commit()
    return True