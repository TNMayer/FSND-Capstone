# Udacity Full Stack Capstone Project

This is the Readme file and also the documentation for my capstone project for Udacity´s Full Stack Developer Nanodegree. To dive right into the app you can use the following endpoint links.

Local API Endoint Link: http://127.0.0.1:8080<br>
Heroku API Endpoint Link: https://tnmayer-fsnd-capstone.herokuapp.com

### Setup local POSTGRES Database

In order to be able to use the endpoints you need a local Postgres endpoint with the same configuration that is used in the application. This can be done via the subsequent psql commands.

First you have to login into your psql command line (e.g. psql -U postgres) and create the production and the test databases.

```
create database fsnd_capstone;
create user fsnd with encrypted password 'fsnd';
grant all privileges on database fsnd_capstone to fsnd;

create database fsnd_capstone_test;
grand all privileges on database fsnd_capstone_test to fsnd;
```

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
Requirements.txt was generated by the following command:
```bash
pip list --format=freeze > requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

### Running the server

From within the `./` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
sh setup.sh
python app.py
```

**Windows users can execute setup.bat instead of sh setup.sh**

## Testing
To run the tests, run
```bash
sh setup.sh
dropdb fsnd_capstone_test
createdb fsnd_capstone_test
python test_app.py
```

## API Documentation

### GET Routes

**GET '/actors'**
- Returns a list of all actors in the database.
- All roles Assistant, Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: get:actors

<details>
<summary>Example Response</summary>

```
{
    "actors": [
        {
            "age": 58,
            "gender": "male",
            "id": 1,
            "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
            "name": "Johnny Depp"
        },
        {
            "age": 57,
            "gender": "male",
            "id": 2,
            "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
            "name": "Russel Crowe"
        }
    ],
    "success": true
}
```

</details>

**GET '/movies'**
- Returns a list of all movies in the database.
- All roles Assistant, Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: get:movies

<details>
<summary>Example Response</summary>

```
{
    "movies": [
        {
            "id": 1,
            "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
            "release_date": "2022-07-31",
            "title": "The Shawshank Redemption"
        },
        {
            "id": 2,
            "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
            "release_date": "2022-05-25",
            "title": "Der Pate"
        }
    ],
    "success": true
}
```

</details>

**GET '/castings'**
- Returns a list of all castings in the database.
- All roles Assistant, Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: get:castings

<details>
<summary>Example Response</summary>

```
{
    "castings": [
        {
            "actor_id": 1,
            "actor_name": "Johnny Depp",
            "id": 1,
            "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
            "movie_id": 1,
            "movie_title": "The Shawshank Redemption"
        },
        {
            "actor_id": 4,
            "actor_name": "Bruce Willis",
            "id": 2,
            "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
            "movie_id": 1,
            "movie_title": "The Shawshank Redemption"
        }
    ],
    "success": true
}
```

</details>

### POST Routes

**POST '/actors'**
- Returns a list of all actors in the database.
- Only roles Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: post:actors

<details>
<summary>Example Request Body</summary>

```
{
    "name": "Marco Sciaini",
    "age": 31,
    "gender": "male"
}
```
</details>
<details>
<summary>Example Response</summary>

```
{
    "actor": {
        "age": 31,
        "gender": "male",
        "id": 13,
        "insertion_datetime": "Sun, 15 Aug 2021 12:22:06 GMT",
        "name": "Marco Sciaini"
    },
    "success": true
}
```

</details>

**POST '/movies'**
- Returns a list of all actors in the database.
- Only role Producer is allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: post:movies

<details>
<summary>Example Request Body</summary>

```
{
    "title": "Trio Infanale",
    "release_date": "2021-07-31"
}
```
</details>
<details>
<summary>Example Response</summary>

```
{
    "movie": {
        "id": 18,
        "insertion_datetime": "Sun, 15 Aug 2021 12:27:57 GMT",
        "release_date": "2021-07-31",
        "title": "Trio Infanale"
    },
    "success": true
}
```

</details>

**POST '/castings'**
- Returns a list of all actors in the database.
- Only role Producer is allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: post:castings

<details>
<summary>Example Request Body</summary>

```
{
    "movie_id": 4,
    "actor_id": 3
}
```
</details>
<details>
<summary>Example Response</summary>

```
{
    "casting": {
        "actor_id": 3,
        "actor_name": "Stefan Reifenberg",
        "id": 9,
        "insertion_datetime": "Sun, 15 Aug 2021 12:31:38 GMT",
        "movie_id": 4,
        "movie_title": "Die Rasselbande aus Riedlingen"
    },
    "success": true
}
```

</details>

### DELETE Routes

**DELETE '/actors/<int: id>'**
- Deletes the actor with the provided ID
- Only roles Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: delete:actors

<details>

<summary>Example Response</summary>

```
{
    "delete": 10,
    "message": "Requested actor AND all related castings successfully removed!",
    "success": true
}
```

</details>

**DELETE '/movies/<int: id>'**
- Deletes the movie with the provided ID
- Only role Producer is allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: delete:movies

<details>

<summary>Example Response</summary>

```
{
    "delete": 8,
    "message": "Requested movie AND all related castings successfully removed!",
    "success": true
}
```

</details>

**DELETE '/castings/<int: id>'**
- Deletes the cating with the provided ID
- Only role Producer is allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: delete:castings

<details>

<summary>Example Response</summary>

```
{
    "delete": 3,
    "success": true
}
```

</details>

### PATCH Routes

**PATCH '/actors/<int: id>'**
- Updates the actor with the given id in the database.
- Only roles Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: patch:actors

<details>
<summary>Example Request Body</summary>

```
{
    "name": "Morgan Freeman",
    "age": 84,
    "gender": "male"
}
```

</details>

<details>
<summary>Example Response</summary>

```
{
    "actors": {
        "age": 84,
        "gender": "male",
        "id": 3,
        "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
        "name": "Morgan Freeman"
    },
    "success": true
}
```

</details>

**PATCH '/movies/<int: id>'**
- Updates the movie with the given id in the database.
- Only roles Director and Producer are allowed to access the endpoint.
- A valid Auth0 token has to be provided via a bearer token in the header of the request.
- Request example is provided in ./test_app.py
- Requires permission: patch:movies

<details>
<summary>Example Request Body</summary>

```
{
    "title": "Die Rasselbandenbude",
    "release_date": "2024-01-05"
}
```
</details>
<details>
<summary>Example Response</summary>

```
{
    "movies": {
        "id": 3,
        "insertion_datetime": "Fri, 06 Aug 2021 14:41:29 GMT",
        "release_date": "2024-01-05",
        "title": "Die Rasselbandenbude"
    },
    "success": true
}
```

</details>