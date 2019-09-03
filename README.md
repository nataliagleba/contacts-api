# Contacts API

- Get list of all Contacts:

`GET: /contacts`

- Search Contacts by username:

`GET: /contacts/?username=<str>`

- Get Contact by id:

`GET: /contact/<id>`

- Create Contact:

`POST: /contact/`

```
payload: {
            'first_name': <str>,
            'last_name': <str>,
            'username': <str>,
            'emails': [<str>, <str>],
        }
```

- Delete Contact:

`DELETE: /contact/<id>`

- Update Contact

`PUT: /contact/<id>/`

# Populate database / Delete contacts older than 1 minute

start redis server

start API app:
`python app.py`

start celery beat:
`celery -A tasks beat --loglevel=info`

start celery worker:
`celery -A tasks worker --loglevel=info`

