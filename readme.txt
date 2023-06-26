Run 
```
docker compose --env-file .env.dev up --build
```
Create superuser : 
```
docker exec -it django-web python manage.py createsuperuser
```

Visit http://localhost:8000 or http://localhost:8000/admin