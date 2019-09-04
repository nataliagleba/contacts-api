#!flask/bin/python
from flask import request, jsonify

from app import app, db
from models import Contact, Email
from schemas import contact_schema, contacts_schema, emails_schema


@app.route("/contacts", methods=["GET"])
def get_contacts():
    username = request.args.get('username')
    if username:
        contacts = Contact.query.filter_by(username=username)
    else:
        contacts = Contact.query.all()

    results = contacts_schema.dump(contacts)
    return jsonify(results)


@app.route("/contacts_delete", methods=["DELETE"])
def delete_all_contacts():
    db.session.query(Contact).delete()
    db.session.commit()
    return jsonify({})


@app.route("/emails", methods=["GET"])
def get_emails():
    all_emails = Email.query.all()
    results = emails_schema.dump(all_emails)
    return jsonify(results)


def create_new_email(address, contact):
    new_email = Email(address, contact)
    db.session.add(new_email)
    db.session.commit()
    return new_email


@app.route("/contact", methods=["POST"])
def add_contact():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    username = request.json['username']
    emails = request.json['emails']

    new_contact = Contact(first_name, last_name, username)
    db.session.add(new_contact)
    db.session.commit()

    if emails:
        for email_address in emails:
            create_new_email(email_address, new_contact)

    return contact_schema.jsonify(new_contact)


@app.route("/contact/<id>", methods=["GET"])
def contact_detail(id):
    contact = Contact.query.get(id)
    return contact_schema.jsonify(contact)


@app.route("/contact/<id>", methods=["PUT"])
def contact_update(id):
    contact = Contact.query.get(id)

    contact.first_name = request.json['first_name']
    contact.last_name = request.json['last_name']
    contact.username = request.json['username']
    contact.emails = []
    db.session.commit()

    emails = request.json['emails']
    for email_address in emails:
        create_new_email(email_address, contact)

    return contact_schema.jsonify(contact)


@app.route("/contact/<id>", methods=["DELETE"])
def contact_delete(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()

    return contact_schema.jsonify(contact)


if __name__ == '__main__':
    app.run(debug=True)
