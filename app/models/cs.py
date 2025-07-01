from app.extensions import db

class CustomerService(db.Model):
    __tablename__ = 'cs'
    admin_id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    logs = db.relationship('Log', back_populates='admin')