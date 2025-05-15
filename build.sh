set -o errexit

python manage.py migrate
python manage.py collectstatic --noinput