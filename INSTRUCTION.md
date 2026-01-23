# DJANGO QUALIFICATION TEMPLATE
## TRIBUTE ALBERT TENINGIN @siriusdevs
### Запуск
```
docker compose up
```
Далее открыть http://localhost/api , появится интерфейс rest_framework

### Запуск тестов
```
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
cd kval
TESTING=1 python manage.py test
```

### Метрики
Перейти на http://localhost/metrics

Названия метрик из задания

HTTP:
- http_requests_total{status_group="total"}
- http_requests_total{status_group="2xx"}
- http_requests_total{status_group="4xx"}
- http_requests_total{status_group="5xx"}

Несуществующие группы появятся при появлении соответствующих запросов

DB:
- django_db_query_duration_seconds_count
- django_db_query_duration_seconds_sum

Частное суммы и количества даст среднее время запроса к базе данных

### Логгирование
Для проверки Correlation ID необходимо выставить заголовок запрос X-Correlation-ID, как в примере ниже:
```
curl http://localhost/api/health/ -H "X-Correlation-ID: abcdefgh"
```
Иначе в логах будет отображён случайный UUID.

Пример лога
```
web-1      | [abcdefgh] django.server INFO "GET /api/health/ HTTP/1.0" 200 0
```