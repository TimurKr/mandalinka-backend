# mandalinka 

This is a web application in development by Timur Kramar.

It is currently designed to work with docker. To run the development server with database run: 

```
docker compose up
```

from the folder containing `docker.compose.yaml`.

Link to open the webpage should be `http://127.0.0.1:8000/`. It will also be specified in the terminal output after the server is started.

For proper functioning, you will need a `secrets` folder, which is not in VS due to safety reasons. To get this folder contact the author.

---
## Useful info for developers:

### Superuser account:
username: admin<br>
email: admin@mandalinka.com<br>
password: admin_heslo<br>

### Accesing servers terminal

```
docker ps
```
```
CONTAINER ID   IMAGE            COMMAND                  CREATED       STATUS         PORTS                                            NAMES
7e94b9fe7cae   mandalinka-web   "python manage.py ru…"   7 weeks ago   Up 4 minutes   0.0.0.0:3000->3000/tcp, 0.0.0.0:8000->8000/tcp   mandalinka-web-1
2d1a483705bb   postgres         "docker-entrypoint.s…"   7 weeks ago   Up 4 minutes   5432/tcp                                         mandalinka-db-1
```

Copy the **CONTAINER ID** from the *mandalinka-web* **IMAGE** (in this case 7e94b9fe7cae) and use it here:

```
docker exec -it <here> bash
```
