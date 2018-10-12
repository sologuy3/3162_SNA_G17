rm -rf .env
mkdir .env
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
cd sna
python manage.py runserver &
google-chrome-stable 127.0.0.1:8000/vis

