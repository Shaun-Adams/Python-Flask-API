# Python-Flask-API

-python -m venv venv
-venv\scripts\activate

-pip install Flask
-pip install flask-sqlalchemy

-python
-from app import db
-db.create_all()

or 
-with app.app_context():
- db.create_all()

- pip install Flask-Migrate
