from app.extensions import db
from datetime import datetime

class Visit(db.Model):
    __tablename__ = 'Visit'
    visit_id = db.Column(db.Integer, primary_key=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.guest_id'))
    purpose = db.Column(db.Text)
    target_service = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    queue_number = db.Column(db.Integer, nullable=True)
    mark = db.Column(db.Enum('hadir','tidak hadir'), default='tidak hadir')

    guest= db.relationship('Guest', back_populates='visits')