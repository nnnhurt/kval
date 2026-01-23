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
