from datetime import datetime
from core import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    linkedId = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    linkPrecedence = db.Column(db.Enum('primary', 'secondary', name='link_precedence'), nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    deletedAt = db.Column(db.DateTime, nullable=True)

    linkedContact = db.relationship('Contact', remote_side=[id], backref='linkedContacts', uselist=False)

    def __repr__(self):
        return f"Contact('{self.id}','{self.email}','{self.phoneNumber}')"

