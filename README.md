# Setup

### Create virtualenv and use it

```
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```

### Run the application

#### Start SQL Proxy

```
./cloud_sql_proxy -instances="koieneres-api-dev:europe-north1:koieneres-api-dev"=tcp:3306
```

### Deploy API
