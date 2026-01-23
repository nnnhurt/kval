# Инструкция квал 
## 1. git clone репозиторий
## 2. cd kval/kval
## 3. Удалить существующую миграцию 0001_initial.py
## 4. Ставим venv
Если выдаст no module named venv, то
```
sudo apt install -y python3-venv

```
если будет какая-то беда в пипом:
```
sudo apt install -y python3-pip
```
## 5. Ставим venv
```
 python -m venv .venv
 source .venv/bin/activate
pip install -r requirements.txt
```
чтобы активировать среду надо открыть любой пайтн файл и внизу справа будет кнопка для выбора среды с версией питона
он или будет в списке, или если нет:
открываю enter interpreter path..
потом find
найти venv потом в нем bin и потом любой python
и нажимаю select
## 6. Переписываем модель
```
python3 manage.py makemigrations
```
## 7. Делаем Сереализатор
## 8. Делаем Вьюсет
## 9. Исправляем путь в urls в app на нынешнюю сущность
## 10. Делаем миграции
## 11. docker compose up --build
## 12. Переходим http://localhost/api
## 13. Проверяем работоспособность теста командой
```
TESTING=1 python manage.py test
```
## 14. Драка с ruff
```
ruff check
ruff check --fix
ruff check
```
## 15. Проверка логирования
выведет abcd в логах
```
curl localhost/api/health/ -H 'X-Correlation-ID: abcde'
```
выведет сгенерированый айди в логах
```
curl localhost/api/health/ 
```
## 16. Prometheus
иду на http://localhost/metrics
и нужны метрики
django_db_query_duration_seconds_count
django_db_query_duration_seconds_sum
и если поделить sum на count, то получится среднее время выполнения запросов в бд

http_requests_total{status_group="2xx"} - количество успешных запросов
http_requests_total{status_group="total"} - тотально
http_requests_total{status_group="4xx"}  - ошибки


### о том как писать валидацию 
```
from django.db import models
from django.core.exceptions import ValidationError

def min_value(value: int) -> None:
    if value < 1000:
        raise ValidationError('>=1000')
# итнвертируем условие чтобы именно выдавал ошибку пон         

class Books(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False, blank=False) # если надо сделать не пустым то null false и blank true
    author = models.CharField(max_length=150)
    published_year = models.IntegerField(validators=[min_value])
    isbn = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
```

и прописываем когда делаю миграцию или когда нужно почистить постгрес и в любой непонятной ситуации
```
docker compose down -v
```



## 17. телепаем сдавать


### Ошибки
если failed to solve: python:3.12-slim: failed to resolve source metadata for docker.io/library/python:3.12-slim: failed to do request: Head "https://registry-1.docker.io/v2/library/python/manifests/3.12-slim": dial tcp: lookup registry-1.docker.io: Temporary failure in name resolution
это ошибка с интернетом, нужно перезапустить докер
```
systemctl restart docker docker.socket
```
2. если он ругается на папку которая создается для сохранения бдшки, то
```
cd ..
sudo rm -r db_kval
cd -
```
3. Error response from daemon: failed to set up container networking: network b2c5635820535bf25dc7cdcc84a85709fdc432e9bbdb7e31ce2ad2d210749a39 not found
стерты все подсети
```
docker compose down -v
docker compose up --build
```
4. если будет говорить на убунте что docker: permission denied или что то такое, то вот такая команда
```
sudo usermod -aG docker $USER
```
и перезайти в пользователя либо лучше вообще перезагрузить комп

5. еще если будут какие то проблемы как вариант почистить все контейнеры докера
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker network prune
# в проекте
docker compose down -v
docker compose up --build
```
да, по порядку, то есть остановить все контейнеры, удалить их, удалить все подсети, потом обязательно сделать docker compose down -v иначе будет ошибка с отсутсвием подсети.
то есть остановить все контейнеры, удалить их, удалить все подсети

## ----
## Ставим venv
### 1. python -m venv .venv
### 2. source .venv/bin/activate

## Ставим Джанго
### 1. pip install django
### 2. pip install djangorestframework
### 3. и просто для подключения к бд 
```
pip install psycopg2-binary
```
## Начинаем проект
### 1. django-admin startproject kval
### 2. cd kval
### 3. django-admin startapp app

# Настройка Settings в project
## 1. LOAD DOTENV
### 1. Ставим pip install python-dotenv
### 2. Пишем в импортах
from dotenv import load_dotenv
from os import getenv
### 3. пишем 
load_dotenv()
### 4. Регистрация приложения в Settings
в INSTALLED_APPS пишем
```
    'app.apps.AppConfig',
    'rest_framework'
```
### 5. Настраиваем БД в Settings
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB', 'db_kval'),
        'USER': getenv('POSTGRES_USER', 'user'),
        'PASSWORD': getenv('POSTGRES_PASSWORD', '1'),
        'HOST': getenv('DB_HOST', 'db_kval'), (Тут обязательно, чтобы было так, как в докеркомпоуз в названии контейнера БД)
        'PORT': getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
        'TEST': {
            'NAME': 'test_kval',
        },
    }
}
```

если же нужен с тестом интеграц то 

```
if getenv('TESTING'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': getenv('POSTGRES_DB', 'db_kval'),
            'USER': getenv('POSTGRES_USER', 'user'),
            'PASSWORD': getenv('POSTGRES_PASSWORD', '1'),
            'HOST': getenv('POSTGRES_HOST', 'db_kval'),
            'PORT': getenv('POSTGRES_PORT', '5432'),
            'OPTIONS': {
                'client_encoding': 'UTF8',
            },
        }
    }
```

## 3. Пишем docker compose 
### 1. Создаем в корне файл docker-compose.yaml
### 2. Прописываем там бд
```
services: 
  db_kval:
    image: postgres:16
    env_file: .env
    volumes:
      - ./db_kval:/var/lib/postgresql/data
    healthcheck: 
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5
```
### 3. Прописываем контейнер для приложения
```
  web_kval:
    build:
      context: . 
    env_file: .env
    volumes: 
      - ./kval:/app
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/api/health/ || exit 1"]
    depends_on:
      db_kval: 
        condition: service_healthy
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
```
### 4. Прописываем контейнер для ngnix 
```
  nginx: 
    image: nginx:mainline
    restart: unless-stopped
    ports:
      - 127.0.0.1:80:80
    volumes:
      - ./default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      web_kval:
        condition: service_healthy
```
### 5. Прописываем config для ngnix в default.conf
```
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://web_kval:8000;  
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Correlation-ID $http_x_correlation_id; # гарантировано пробросит заголовок
    }
}
```
### 6. Создаем Dockerfile в корне и пишем:
```
FROM python:3.12-slim
# добавляем юникс группу и пользователя
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --gid 1001 appuser


WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# меняем владельца директории на appuser:appgroup
RUN chown -R appuser:appgroup /app

# переключаемся на appuser
USER appuser

```
## 4. Пишем модели
```
from django.db import models

class Students(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```
## 5. Пишем миграции
```
python3 manage.py makemigrations
```
внутри докер компоуз должно выполняться python3 manage.py migrate, поэтому внутри в конце докер компоуз команду
```
  web_kval:
    build:
      context: . 
    env_file: .env
    volumes: 
      - ./kval:/app
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:8000/api/health/ || exit 1"]
    depends_on:
      db_kval: 
        condition: service_healthy
    command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

```
эту команду в конец 
```
command: sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
```
## 6. Делаем .env
```
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
```
Чтобы просто рестартануть докер, даже если с build нет, то systemctl restart docker docker.socket
## 7. Requirements
```
pip freeze > requirements.txt
```
## 8. Запускаем докер
```
docker compose up
```
## 9. Пишем Serialializer
Создаем в app новый файл и называем serialializers.py
```
from rest_framework import serializers
from .models import Students

class StudentSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Students
        fields = '__all__'
```
## 10. Пишем Viewset
В app в views.py
```
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Students
from .serializers import StudentSerializer

def health_check(request):
    return JsonResponse({"status":"ok"})

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentSerializer
    permission_classes = []

```
## 11. URLS в app
Создаем в app файл urls.py
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, health_check

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check) # для healthcheck и интеграц теста
]
```
Если же несколько сущностей, мы их прописываем так
```
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, health_check

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'....')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check) # для healthcheck и интеграц теста
]
```
## 12. URLS в основной
Здесь мы именно само приложение подключаем к проекту
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')),
]
```

## 13. драка с компоуз
если он ругается на папку которая создается для сохранения бдшки, то
```
cd ..
sudo rm -r db_kval
cd -
```
или в конце докер компоуз
```
volumes:
    db_kval(папка с бд):
```
## 14. идем на http://localhost:8080/api/

## 15. Пишем тест
В app пустой файл tests.py, туда:
```
from django.test import TestCase, Client


class HealthCheckIntegrationTest(TestCase):
    def setUp(self) -> None:
        self.client: Client = Client()
    
    def test_health_check_returns_200(self) -> None:
        response = self.client.get('/api/health/')
        
        self.assertEqual(response.status_code, 200)
```
запуск теста
```
TESTING=1 python manage.py test
```

## 16. Prometheus
Ставим pip install django-prometheus
Обновляем зависимости
потом в INSTALLED APP в Settings
"django_prometheus", после в MEADLEWEAR 

После в kval urls.py в конец
```
path('', include('django_prometheus.urls')),
```


```
