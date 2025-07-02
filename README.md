чтобы запустить через docker в bash перейдите в папку с проектом и введите docker-compose up --build
если хотите проверить на локальной машине разверните окружение, импортните requirements.txt
в .env поменяйте POSTGRES_HOST c db на localhost
и выполните python manage.py runserver

POSTGRES_DB=item_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_HOST=db
POSTGRES_PORT=5432

SECRET_KEY=django-insecure-q82dkj8@)#8$3jy092436e*ymtf*zg$uz!055g--uwkwo#+mo&
