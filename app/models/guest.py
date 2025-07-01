from app.extensions import db

class Guest(db.Model):
    __tablename__ = 'guest'
    guest_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    guest_name = db.Column(db.String(100))
    gender = db.Column(db.Enum('L','P'))
    identity_type = db.Column(db.String(50))
    identity_number = db.Column(db.String(50))
    institution = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    visits = db.relationship('Visit', back_populates='guest',cascade="all, delete-orphan")
