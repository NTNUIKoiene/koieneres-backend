# Setup

### Create virtualenv and use it

```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

### Running the application locally

#### Create dotenv file

Create a file called `.env` and add the required secrets:

```
DB_HOST=[CONNECTION URL]
DB_PORT=[PORT]
DB_NAME=[DB NAME]
DB_USER=[DB USERNAME]
DB_PASSWORD=[DB PASSWORD]
SECRET=[DJANGO SECRET KEY]
EMAIL_HOST_USER=[EMAIL USER]
EMAIL_HOST_PASSWORD=[EMAIL PASSWORD]
EMAIL_HOST=[SMTP HOST]
EMAIL_PORT=[SMTP PORT]
EMAIL_USE_TLS = True
SENTRY_DSN=[SENTRY_DSN]
```

#### Migrate the database

```
python manage.py migrate
```

#### Start the application

```
python manage.py runserver
```

# CI/CD

Changes to the `master`-branch are automatically deployed to production.

## Sentry

Koieneres uses [Sentry](https://sentry.io) to log errors that occur in production.

# Server Setup

The application runs on DigitalOcean using docker-compose. Docker-compose manages nginx and certificates. The only software required on the server is docker and docker-compose(`snap install docker`). To refresh certificates add the following line to the crontab file:

```
0 12 * * * /root/koieneres-backend/ssl_renew.sh >> /var/log/cron.log 2>&1
```

The setup is inspired by [this guide](https://www.digitalocean.com/community/tutorials/how-to-secure-a-containerized-node-js-application-with-nginx-let-s-encrypt-and-docker-compose).
