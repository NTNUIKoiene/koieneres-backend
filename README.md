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
DB_HOST=/cloudsql/[CONNECTION NAME]
DB_NAME=[DB NAME]
DB_USER=[DB USERNAME]
DB_PASSWORD=[DB PASSWORD]
SECRET=[DJANGO SECRET KEY]
```

#### Start SQL Proxy

```
./cloud_sql_proxy -instances="koieneres-api-dev:europe-north1:koieneres-api-dev-db"=tcp:3306
```

This proxy enables the Django application running locally to communicate with the SQL database in Google Cloud.

### Deploy API

#### Digitalocean and docker:

https://www.digitalocean.com/community/tutorials/how-to-secure-a-containerized-node-js-application-with-nginx-let-s-encrypt-and-docker-compose

#### Create secret config file

Create a file called `env.yaml` and add the required secrets:

```
env_variables:
  DB_HOST: "/cloudsql/[CONNECTION NAME]"
  DB_NAME: [DB NAME]
  DB_USER: [DB USERNAME]
  DB_PASSWORD: [DB PASSWORD]
  SECRET: [DJANGO SECRET KEY]
```

#### Collect static files

```
python manage.py collectstatic
```

#### Deploy

```
gcloud app deploy
```
