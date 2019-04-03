FROM python:3.6.6


ENV APP_HOME /koieneres-backend
ENV PYTHONPATH $APP_HOME
ENV PYTHONUNBUFFERED 1
ENV ENV_CONFIG 1
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

COPY requirements.txt $APP_HOME/requirements.txt
RUN pip install -r requirements.txt

RUN set -e && \
  pip install --upgrade pip && \
  pip install --no-cache-dir uwsgi

COPY .env $APP_HOME/.env
COPY ./ $APP_HOME 

RUN python manage.py 
RUN python manage.py collectstatic --noinput

EXPOSE 8000


ENV UWSGI_WSGI_FILE=koieneres/wsgi.py UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

CMD set -e && \
  python manage.py migrate && \
  uwsgi --log-x-forwarded-for --http-auto-chunked --http-keepalive --static-map /static=$APP_HOME/static
