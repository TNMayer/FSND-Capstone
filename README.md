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

**GET '/actors'**
- Fetches a list of all actors in the database.
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

**GET '/questions?page=${integer}'**
- Fetches a paginated set of questions, a total number of questions, all categories and current category string. 
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 100,
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" },
    'currentCategory': 'History'
}
```

**GET '/categories/${id}/questions'**
- Fetches questions for a cateogry specified by id request argument 
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 4
        },
    ],
    'total_questions': 100,
    'currentCategory': 'History'
}
```

**DELETE '/questions/${id}'**
- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Returns the success status and the id of the deleted question

```
{
    'success': True,
    'deleted': question_id
}
```

**POST '/quizzes'**
- Sends a post request in order to get the next question 
- Request Body:
```
{
    'previous_questions':  an array of question id's such as [1, 4, 20, 15]
    'quiz_category': a string of the current category 
}
```
- Returns: a single new question object
```
{
    'question': {
        'id': 1,
        'question': 'This is a question',
        'answer': 'This is an answer', 
        'difficulty': 5,
        'category': 4
    }
}
```

**POST '/questions'**
- Sends a post request in order to search for a specific question by search term 
- Request Body: 
```
{
    'searchTerm': 'this is the term the user is looking for'
}
```
- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string
```
{
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 5
        },
    ],
    'total_questions': 100,
    'current_category': None
}
```

**POST '/questions'**
- Sends a post request in order to add a new question
- Request Body:
```
{
    'question':  'Heres a new question string',
    'answer':  'Heres a new answer string',
    'difficulty': 1,
    'category': 3
}
```
- Returns:
```
{
    'success': True,
    'created': 98,
    'question_created': 'Heres a new question string',
    'questions': [
        {
            'id': 1,
            'question': 'This is a question',
            'answer': 'This is an answer', 
            'difficulty': 5,
            'category': 2
        },
    ],
    'total_questions': 250
}
```
