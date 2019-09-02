from datetime import datetime

from extensions import db


class Contact(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, index=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    emails = db.relationship('Email', backref='contact_emails', cascade='delete, delete-orphan')

    def __init__(self, first_name, last_name, username):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

    def __unicode__(self):
        return u'Contact id: {}, Last name: {}'.format(
            self.id,
            self.last_name,
        )

    def __repr__(self):
        return self.__unicode__().encode('utf8')


class Email(db.Model):
    __tablename__ = 'emails'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(50))

    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)
    contact = db.relationship('Contact', backref='email_contact')

    def __init__(self, address, contact):
        self.address = address
        self.contact = contact

    def __unicode__(self):
        return u'Email Address: {}'.format(
            self.address,
        )

    def __repr__(self):
        return self.__unicode__().encode('utf8')
