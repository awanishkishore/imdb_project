# IMDB Project


### How to set it up?
<br/>

#### Method 1: Normal setup
**Prequisites**<br/>
Following dependencies must be installed in your system:
- Postgres
- Python 3.8 or above

**Steps**
1. Clone this repository.
2. Create .env file in root directory. (Contents of .env is present below.)
3. Install requirements.txt using command `pip install -r requirements.txt`
4. Migrate migration files using `python manage.py migrate`
5. To create admin user, run `python manage.py createsuperuser`
6. Start web server with `python manage.py runserver`
7. Load DB dump using `python manage.py loaddata ./extras/db_dump.json`
<br/><br/>

#### Method 2: Docker setup
**Prequisites**<br/>
Following dependencies must be installed in your system:
- Docker & Docker Compose

**Steps**
1. Clone this repository.
2. Create .env file in root directory. (Contents of .env is present below.)
3. Set `IS_DOCKERIZED=1` in .env file.
4. Run `docker-compose up --build -d`
5. Run `docker exec -it imdb_service /bin/bash`
6. Now migrate migration files using `python manage.py migrate`
7. To create admin user, run `python manage.py createsuperuser` (This is the only way an admin user can be created.)
8. Load DB dump using `python manage.py loaddata ./extras/db_dump.json`
9. Server will be running on port 8000.
<br/><br/>

### What has been covered in this project?
1. API to search for a movie with name which will provide movie’s information, it’s average rating, count of people who have rated the returned movie, comments.
2. API where a user can see movies that he has rated and his comments on those movies.
3. API to rate a movie
4. API to add comment on movie
5. Guest users would be able to search for a specific movie by movie name.
6. Logged In users would be able to rate a movie or comment on it.
7. Admin users would be able to add new movies, documentaries and shows to which users will rate and comment.
<br/><br/>

### How to test this project?
- All the endpoints with CURL commands & corrosponding examples are publised [here](https://documenter.getpostman.com/view/11856231/TVsoJBTd)
- Postman collection is present in extras folder.
- Use auth header as "Authorization": "Token <token_value>"
<br/><br/>


#### .env example
```yaml
SECRET_KEY=whatever_secret_you_want_to_keep

### DB Settings ###
POSTGRES_DB=imdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_PORT=5432

IS_DOCKERIZED=0
```