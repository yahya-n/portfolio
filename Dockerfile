FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install build tools and system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /code/

RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . /code/

RUN python manage.py collectstatic --noinput

CMD sh -c "python manage.py migrate && \
           python manage.py createsuperuser --noinput || true && \
           python -c 'import os; import django; django.setup(); from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username=os.environ[\"DJANGO_SUPERUSER_USERNAME\"]); user.set_password(os.environ[\"DJANGO_SUPERUSER_PASSWORD\"]); user.save()' && \
           python -c 'import gevent; print(gevent.__version__)' && \
           gunicorn about.wsgi:application --bind 0.0.0.0:$PORT --worker-class gthread --workers 2 --threads 4 --timeout 60"
