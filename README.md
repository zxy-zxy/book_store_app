## Book store CRUD application.
A simple CRUD application 
### To run on local machine:

```bash
python manage.py loaddata fixtures/data.json --settings=bookstore.settings.local_development
python manage.py createsuperuser --settings=bookstore.settings.local_development
python manage.py runserver --settings=bookstore.settings.local_development
```

