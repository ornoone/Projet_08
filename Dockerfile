FROM python:3
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE Projet_08.settings.prod

RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y \
    cron \
    automake \
    build-essential \
    curl \
    dpkg-sig \
    libcap-dev \
    supervisor \
    nginx \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
COPY projet_08-nginx /etc/nginx/sites-available/purbeurre
RUN rm /etc/nginx/sites-enabled/default && ln -s /etc/nginx/sites-available/purbeurre /etc/nginx/sites-enabled
COPY projet_08-supervisor.conf /etc/supervisor/conf.d/
RUN python /code/manage.py collectstatic --noinput

CMD ["/usr/bin/supervisord", "-n"]