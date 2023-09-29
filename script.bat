python -m venv venv
call venv/scripts/activate
pip install -r requirements.txt

flask --app main run --host=0.0.0.0 --port=8000 --debug

cmd