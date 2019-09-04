from datetime import datetime, timedelta
from flask import json
import os

from api import *
from schemas import contact_schema
from tasks import delete_contacts, populate_contacts


class TestContactsService():
    def setup(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')
        db.create_all()
        self.insert_contacts_into_db()

    def insert_contacts_into_db(self):
        contact_no_1 = Contact('first name', 'last name', 'username1')
        contact_no_1.id = 1
        contact_no_1.created_at = datetime.utcnow() - timedelta(minutes=2)
        db.session.add(contact_no_1)

        new_email = Email('test_email@test.com', contact_no_1)
        db.session.add(new_email)

        contact_no_2 = Contact('name', 'surname', 'username')
        db.session.add(contact_no_2)

        db.session.commit()

    def teardown(self):
        db.session.remove()
        db.drop_all()


class TestTasks(TestContactsService):
    def test_delete_contacts(self):
        assert Contact.query.count() == 2

        task = delete_contacts.s().apply()
        assert task.status == 'SUCCESS'
        assert Contact.query.count() == 1

    def test_add_contacts(self):
        assert Contact.query.count() == 2

        task = populate_contacts.s().apply()
        assert task.status == 'SUCCESS'
        assert Contact.query.count() == 3


class TestAPI(TestContactsService):

    def test_add_contact(self):
        response = app.test_client().post(
            '/contact',
            data=json.dumps({"first_name": "Nat",
                             "last_name": "Gle",
                             "username": "natgle",
                             "emails": ["natgle@gmail.com"]}),
            content_type='application/json')

        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert data['username'] == 'natgle'

        # test contact object was created
        assert Contact.query.filter_by(username='natgle')

        # test email address object was created
        assert Email.query.filter_by(address='natgle@gmail.com')

    def test_get_all_contacts(self):
        response = app.test_client().get(
            '/contacts')

        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 2

    def test_search_contacts_by_username(self):
        response = app.test_client().get(
            '/contacts' + '?username=username1')

        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 1

    def test_get_contact_by_id(self):
        response = app.test_client().get(
            '/contact/1')

        data = json.loads(response.data)
        assert response.status_code == 200

        contact_no_1 = Contact.query.get(1)
        assert data == contact_schema.dump(contact_no_1)

    def test_update_contact_by_id(self):
        response = app.test_client().put(
            '/contact/1',
            data=json.dumps({"first_name": "Nat",
                             "last_name": "Gle",
                             "username": "natgle",
                             "emails": ["natgle@gmail.com"]}),
            content_type='application/json')

        assert response.status_code == 200

        contact_no_1 = Contact.query.get(1)
        assert contact_no_1.username == 'natgle'
        assert contact_no_1.first_name == 'Nat'
        assert contact_no_1.last_name == 'Gle'

        email = Email.query.filter_by(contact=contact_no_1, address='natgle@gmail.com').first()
        assert email
        assert contact_no_1.emails == [email]

    def test_delete_contact(self):
        assert Contact.query.get(1)

        response = app.test_client().delete(
            '/contact/1')

        assert response.status_code == 200
        assert not Contact.query.get(1)
