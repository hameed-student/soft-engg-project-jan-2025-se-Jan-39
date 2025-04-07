set FLASK_APP=backend/app.py
flask db init
flask db migrate
flask db upgrade
python backend/admin.py
flask run
