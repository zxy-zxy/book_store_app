## Book store CRUD application.
A simple CRUD application. 

Application contians few models:
* Book model
* Publisher model
* Author model

Book model is available to create and update for logged-in users. Before run, you may need to create superuser, 
and load fixtures with some relevant data.


### To run on local machine:

```bash
python manage.py loaddata fixtures/data.json --settings=bookstore.settings.local_development
python manage.py createsuperuser --settings=bookstore.settings.local_development
python manage.py runserver --settings=bookstore.settings.local_development
```
### To run tests:
```bash
python manage.py test --settings=bookstore.settings.local_development 
```
