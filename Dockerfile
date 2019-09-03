FROM ubuntu:19.04
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=books_talk.settings.container

RUN apt-get update && apt-get install -y nginx python3-dev python3-pip python3-setuptools python3-wheel
WORKDIR /app
COPY requirements ./requirements/
RUN pip3 install --no-cache-dir -r requirements/base.txt && pip3 install --no-cache-dir gunicorn

COPY nginx.conf /etc/nginx/nginx.conf
COPY books_talk ./books_talk/

EXPOSE 80
CMD nginx && gunicorn --bind unix:/tmp/gunicorn.sock --timeout 1800 --workers 5 --chdir books_talk books_talk.wsgi:application
