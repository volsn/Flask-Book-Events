# Flask Book Events

Aditional service for [Django Book Reviews](https://github.com/volsn/Django-Book-Reviews), that uses data about users and authors taken from REST Endpoints to sign them for events as guests or participants.


Technologies used in this Project:

- Flask
- Flask-RESTFul
- Flask-Admin
- Flask-Babel
- SQLAlchemy
- Marshmallow
- JWT
- Faker

## Run
___

Run with builtin Flask Server 

```bash
$ pip install -r requirements.txt
$ python app.py
```

## Data

All Data downloaded and cleaned from [Kaggle](https://www.kaggle.com/zygmunt/goodbooks-10k?select=books.csv)

## Populate

App includes a [script](populate.py) for populating database with authors from Kaggle Dataset as well as fake data about events and guests.