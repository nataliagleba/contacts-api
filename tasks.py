from celery import Celery
from datetime import datetime, timedelta
import random

from models import Contact, Email
from app import db

celery = Celery('periodic', broker='redis://localhost:6379/0')

celery.conf.beat_schedule = {
    "populate_contacts_every_fifteen_seconds_task": {
        "task": "tasks.populate_contacts",
        "schedule": 15.0
    },
    "delete_contacts_every_fifteen_seconds_task": {
        "task": "tasks.delete_contacts",
        "schedule": 15.0

    }
}


@celery.task()
def populate_contacts():
    random_value = str(random.randint(0, 1000))
    data = {
        'first_name': 'first_name_' + random_value,
        'last_name': 'last_name_' + random_value,
        'username': 'user_' + random_value,
    }
    emails = [random_value + '@test.com', random_value + '@test.co.uk']
    new_contact = Contact(**data)
    db.session.add(new_contact)

    for address in emails:
        new_email = Email(address, new_contact)
        db.session.add(new_email)

    db.session.commit()

    print("Created new contact")


@celery.task()
def delete_contacts():
    now = datetime.utcnow()
    items_deleted = db.session.query(Contact).filter(Contact.created_at < now - timedelta(minutes=1)).delete()
    db.session.commit()
    print("deleted {} items".format(items_deleted))
