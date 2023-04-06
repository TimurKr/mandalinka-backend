# Mandalinka backend

## About

This is the backend service for mandalinka. It provides GraphQL endpoint at the root url `/` and admin page at `/admin`

Related repositories: 
- [web app](https://github.com/TimurKr/mandalinka-web)

## Development

To run this server in development, follow these steps:

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

> If the repozitory was just cloned, intelisense will not work. Run in the development to create the virtual environment with all requirements and than select the interpreter from the `venv`.

## Deployment

1. Run 
```
gcloud app deploy
```

#### Working on:

Simplifying running in development and CI/CD using GitHub Actions is in proccess.

The deployement shoud be as simple as merging a branch/pushing to master. Github actions should take care of:
- collecting static files
- running tests
- migrating database
- deploying to Google Cloud App Engine

## Useful info for developers:

### Superuser account:

username: admin<br>
email: admin@mandalinka.sk<br>
password: admin_heslo<br>
