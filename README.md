# Mandalinka backend

This is the backend service for mandalinka. It provides GraphQL endpoint at the root url `/` and admin page at `/admin`

Related repositories: 
- [web app](https://github.com/TimurKr/mandalinka-web)

---

## Currently working on

Simplifying running in development and CI/CD using GitHub Actions is in proccess.

The endgoal is that upon cloning this directory, starting development server will be as simple as running starting a virtual environment and running
```
python manage.py runserver
```
The deployement shoud be as simple as merging a branch/pushing to master. Github actions should take care of:
- collecting static files
- running tests
- migrating database
- deploying to Google Cloud App Engine

---

## Useful info for developers:

### Superuser account:

username: admin<br>
email: admin@mandalinka.sk<br>
password: admin_heslo<br>
