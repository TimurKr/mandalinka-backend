# mandalinka

This is a the backend for mandalinka project. It provides GraphQL endpoint at the root url `/` and admin page at `/admin`

It is currently designed to work with docker. To run the development server with database run:

```
docker compose -f docker-compose.yml -f docker-compose.debug.yml up --build
```

from the folder containing `docker.compose.yaml`.

Link to the webpage is: `http://localhost:8000/`. 

For proper functioning, you will need a `secrets` folder, which is not in VS due to safety reasons. To get this folder contact the author.

---

## Useful info for developers:

### Superuser account:

username: admin<br>
email: admin@mandalinka.sk<br>
password: admin_heslo<br>

### Accesing servers terminal

Idealy use `Docker` plugin for VS Code. Right click athe desired container and select `attach shell`. 

Alternatively list the running containers
```
docker ps
```
and than run shell in the desired, using the `CONTAINER ID`:
```
docker exec -it <CONTAINER_ID> bash
```
