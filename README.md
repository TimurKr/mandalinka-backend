# Mandalinka backend

## About

This is the backend service for mandalinka. It provides GraphQL endpoint at the root url `/` and admin page at `/admin`

Related repositories:

- [web app](https://github.com/TimurKr/mandalinka-web)

## Development

##### Running server in development

1. Make sure you have downloaded gcloud CLI. [How?](https://cloud.google.com/sdk/docs/install)
2. Initialize `gcloud` by running

```
gcloud init
```

3. Authenticate `gloud` by running

```
gcloud auth application-default login
```

4. Run the server with the script

```
./run_development.sh
```

This runs the script in a virtual environment.

##### Running django commandse using `manage.py`

1. Run in parallel with the server

- Run the server in one terminal `./run_development.sh`
- Open new terminal and activate the virtual environment `source venv/bin/activate`. It will be activated automatically if using VSCode and you have selected the interpreter from the `venv`.
- Run `export DEVELOPMENT=True` to add the required environment variable
- Run the command in the new terminal `python manage.py <command>`

2. Run without running the server

- Activate the virtual environment `source venv/bin/activate`. It will be activated automatically if using VSCode and you have selected the interpreter from the `venv`.
- Start the Cloud SQL proxy. If it is not dowloaded, run the development script once to download it.

```
./cloud_sql_proxy -instances=mandalinka-275618:us-central1:mandalinka-db=tcp:5432
```

- Set the environment variables `export DEVELOPMENT=True`
- Run the command `python manage.py <command>`

> If the repozitory was just cloned, intelisense will not work. Run in the development to create the virtual environment with all requirements and then select the interpreter from the `venv`.

## Deployment

The app is deployed to Google Cloud App Engine. The deployment is done using GitHub Actions. The deployment is triggered when a new commit is pushed to the master branch. Avoid pushing to master directly. Create a new branch and create a pull request to master.
Do not deploy deploy to production directly.

#### Working on:

## Useful info for developers:

### Superuser account:

username: admin
email: admin@mandalinka.sk
password: admin_heslo
