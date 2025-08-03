# Dockerfile
FROM python:3.12-slim
LABEL maintainer="rjross3378@gmail.com"

# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure logs are output directly
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
