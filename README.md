Project Configuration

1) Install all dependencies
	pip install -r requirements.txt

2) Set database settings and Github credentials in config.sh file and run
	. ./config.sh

3) Run migrations
	python manage.py migrate

4) Run the project
	python manage.py runserver