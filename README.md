## Lab: 33 - Authentication & Production Server


### Estimate of time needed to complete: 4 hours
### Start time: at 1/12/2021 4:30 pm
### Finish time: at 1/14/2021 7:17 pm
### Actual time needed to complete: 3 hours

-----------------------------------------------

# How To install | Full Guide By Omar Zain

- install doker if you didn't from here: `https://www.docker.com/get-started`
- `mkdir drf-api`
- `cd drf-api`
- `poetry init -n`
- `poetry add django djangorestframework`
- `poetry shell`
- `django-admin startproject digimon_project .`
- `python manage.py  migrate`
- `python manage.py  startapp digimon`
- `python manage.py  createsuperuser`
- `python manage.py  runserver`
______________________________________________
- in the `settings.py` ---> INSTALLED_APPS --->add the app to project applications `'digimon.apps.digimonConfig',`
- go to `digimon/models.py` ----> 
```python
from django.contrib.auth import get_user_model
from django.db import models

class Digimon(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

```
- `python manage.py makemigrations digimon`
- `python manage.py migrate`

- go to  digimon/`admin.py` ----> add :
```python
from django.contrib import admin

from .models import Digimon
# Register your models here.

admin.site.register(Digimon)

```
- `python manage.py runserver`
- do tests
- in the `settings.py` ---> INSTALLED_APPS --->add the app to project applications `'rest_framework',`
- in the `settings.py` add:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASS': [
        'rest_framework.permissions.AllowAny',
    ]
}
```
- in digimon_project/`urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/digimon/', include('digimon.urls')),
]

```

- create digimon/`serializer.py` to convert data to json:
```python
from rest_framework import serializers

from .models import digimon

class digimonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'author', 'body', 'created_at')
        model = digimon

```
- in digimon/`views.py`:
```python 
from django.shortcuts import render
from rest_framework import generics

from .models import digimon
from .serializer import digimonSerializer

class digimonList(generics.ListCreateAPIView):
    queryset = digimon.objects.all()
    serializer_class = digimonSerializer

class digimonDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = digimon.objects.all()
    serializer_class = digimonSerializer
```
- in digimon/`urls.py`:
```python
from django.urls import path

from .views import digimonList, digimonDetails

urlpatterns = [
    path('', digimonList.as_view(), name='digimon'),
    path('<int:pk>/', digimonDetails.as_view(), name='digimon_details') 
]

```
- `python manage.py  runserver`
- in root create `Dockerfile` inside it write:
```
FROM python:3
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
```
- in root create `docker-compose.yml` inside it write:
```
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"

```
- in the `settings.py` --->add `ALLOWED_HOSTS = ['0.0.0.0',]`
- `python manage.py runserver 0.0.0.0:8000`
- `poetry export -f requirements.txt -o requirements.txt`
- open docker
- `docker-compose up`
- if it didnt work:
- open docker-->dashboard --->start--->open in window  settings#ALLOWED_HOSTS = ['0.0.0.0','localhost','127.0.0.1']
- or try:
- `docker-compose down`
- `docker-compose build`
- `docker-compose up`
_______________________________________________________________________________________

# permissions
- `poetry shell`
- `poetry install`
- `python run server`
- `python run server`
- go `settings.py` edit :
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASS': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

```
- go to `digimon_project/urls.py` add to urlpatterns `path('api-auth', include('rest_framework.urls')),`
- create `digimon/permissions.py` add inside it :
```python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True


        return obj.author == request.user

```
- go to `digimon/views.py` add:
```python 
from .permissions import IsAuthorOrReadOnly
#to class digimonDetails add:
permission_classes = (IsAuthorOrReadOnly,)

```
- ` python manage.py runserver`



# postgres
- go to `settings.py` :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

```
- edit`docker-compose.yml` :
```python
version: '3'

services:
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/code
    ports:
      - "8000:8000"
    depends_on:
        - db
  db:
      image: postgres:11
      environment:
          - "POSTGRES_HOST_AUTH_METHOD=trust"

```
- `poetry add psycopg2`
- `poetry export -f requirements.txt -o requirements.txt`
- exit poetry
- `docker-compose run web python manage.py makemigrations `
- `docker-compose run web python manage.py migrate `
- `docker-compose run web python manage.py createsuperuser `
- `docker-compose up`
- to run test :
- `docker-compose run web python manage.py test`
_______________________________________________________________________
# tokens
- `poetry add djangorestframework_simplejwt` make sure to change pyproject.toml--> `python = "~3.8"`
- `poetry add gunicorn` # Running Django in Gunicorn as a generic WSGI application/to run production mode
- `poetry add whitenoise`# allows your web app to serve its own static files, making it a self-contained
- `poetry export -f requirements.txt -o requirements.txt`
- go to `settings.py` add:
```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],#for tokens+ to let me login
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}
```
- go to `digimon_project/urls.py`add :
```python
from rest_framework_simplejwt import views as jwt_views
#in urlpatterns add:
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
```
- in `docker-compose.yml` edit :
```
version: '3.8'
command: gunicorn digimon_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

- in `settings` add:# to add css 
```python
import os
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR,
]
```
- in `settings` add: # to add css 
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # <<<<<<<<<<<<<< add this
    'django.contrib.staticfiles',

    'rest_framework',

    'digimon.apps.digimonConfig',

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <<<<<<<<<<<<<< add this
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

```
- `docker-compose up --build`
- click `inspect` --> `application`--> you can find your token

- or play with `pip install httpie`
- http POST 127.0.0.1:8000/api/token/ username='your username' password='your password'
- http GET 127.0.0.1:8000/api/v1/plants/ "Authorization: Bearer your token key"

- or try postman

