from app.extensions import db
from datetime import datetime, timedelta

def default_expired_at():
    return datetime.utcnow() + timedelta(days=7)
class Log(db.Model):
    __tablename__ = 'Log'
    log_id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('cs.admin_id'), nullable=True)
    admin_env = db.Column(db.String(64), nullable=True)  # Untuk admin dari .env
    action = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    expired_at = db.Column(db.DateTime, nullable=True, default=default_expired_at)

    admin = db.relationship('CustomerService', back_populates='logs')