from celery import Celery
from datetime import datetime, timedelta
import random
import requests

from models import Contact
from extensions import db

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
    payload = {
        'first_name': 'first_name_' + random_value,
        'last_name': 'last_name_' + random_value,
        'username': 'user_' + random_value,
        'emails': [random_value + '@test.com', random_value + '@test.co.uk']
    }
    requests.post('http://localhost:5000/contact', json=payload)
    print("Created new contact")


@celery.task()
def delete_contacts():
    now = datetime.utcnow()
    items_deleted = db.session.query(Contact).filter(Contact.created_at < now - timedelta(minutes=1)).delete()
    db.session.commit()
    print("deleted {} items".format(items_deleted))
