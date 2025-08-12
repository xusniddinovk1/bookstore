ONLINE BOOKSTORE

Quick start (local)

1.Create and activate virtual environment:
python -m venv venv venv/bin/activate or venv\Scripts\activate on Windows

2.Install packages:
pip install -r requirements.txt

3.Apply migrations:
python manage.py makemigrations, python manage.py migrate

4.Create superuser:
python manage.py createsuperuser

5.Run Django server:
python manage.py runserver
