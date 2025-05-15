release: python manage.py migrate
web: gunicorn vinilos.wsgi --timeout 120 --workers 4