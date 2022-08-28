# Udacitrivia Application

Udacitrivia is a gaming application. It allow users to manage questions and play game. This application is splitted into tow (2) categories.

1. Backend - The backend is built with Python technology using the Flask Python framework with Postgresql as the database.
2. Frontend - The frontend is built with ReactJS.

All backend code follows [PEP8 Style Guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

To get started with this application, you must have python3, pip, postgresql and node installed

#### Backend

## Installation

To run this app flawlessly, satisfy the requirements. First, navigate to the backend folder and create virtual environment

On Windows

```bash
py -3 -m venv your_venv_name
```

On Mac

```bash
python3 -m venv your_venv_name
```

Next, make sure to select the interpreter in the virtual environment you just create and not the global interpreter. To do that, go to the path where the interpreter reside.

On Windows

```bash
venv\Scripts\python.exe
```

On Mac

```bash
venv\bin\python.exe
```

Next, activate the environment you just created by running the following command on your command line

On Windows

```bash
venv\Scripts\activate
```

On Mac

```bash
source venv\bin\activate
```

Next, it is now time to install the dependencies which is located inside backend folder.

```bash
pip3 install -r requirements.txt
```

Note: If pip3 doesn't work for you, you can as well switch to using pip

### Set up the Database

Start a postgres server using the default postgres username and password

```bash
psql -U postgres
```

You will be required to enter your database.

With Postgres running, create a `trivia` database from the command line:

```bash
createbd trivia
```

or run this command

```bash
CREATE DATABASE trivia
```

Connect to the database you just created by running the following command

```bash
\c trivia
```

Populate the database using the `trivia.psql` file provided. This is up to you. You can skip this stage and create your own records from scratch.
To continue, from the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

or run this command

```bash
\i path/to/your/backend/trivia.psql
```

## Set Environment Variables

Next, we have to setup the environment variables to be able to run flask app successfully

On Windows

```bash
set FLASK_APP=app.py
set FLASk_ENV=development
```

On Mac

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
```

## Start Server

To run the application run the following commands:

```bash
flask run
```

Or run this command

```bash
$ python -m flask run
```

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

Note: if you experience any difficulty starting the server which is the backend, follow the following steps

1. Pip uninstall the dependencies which you installed earlier (requirements.txt)
2. Go to requirements.txt file, remove version numbers from each dependency
3. Pip install them again

### Tests

In order to run tests navigate to the backend folder and run the following commands:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command.

### Frontend

From the frontend folder, run the following commands to start the client:

```bash
npm install // only once to install dependencies
npm start
```

Note: if you experience any difficulty starting the client which is the frontend, delete the node_modules folder and package-lock.json file and run npm install again.

## API Reference

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
    "success": False,
    "error_code": 400,
    "message": "bad request"
}
```

Udacitrivia API will return six (6) error types when requests fail:

- 400: bad request
- 404: resource not found
- 405: method not allowed
- 409: request conflicts
- 422: unprocessable
- 500: internal server error

### Endpoints

#### GET /api/v1/categories

- General:
  - Returns a list of categories objects, and success value
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/categories`

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

#### POST /api/v1/categories

- General:
  - Creates a new category using the submitted type.
  - Returns the id of the created category, success value, and a message key.
- `curl http://127.0.0.1:5000/api/v1/categories -X POST -H "Content-Type: application/json" -d '{"type":"Politics"}'`

```bash
{
  "category_id": 7,
  "message": "Category created successfully",
  "success": true
}
```

#### GET /api/v1/category/{category_id}/questions

- General:
  - Returns a list of questions objects, current_category, total_questions and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/categories/6/questions?page=1`

```bash
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "London",
      "category": 6,
      "created_at": "Sat, 27 Aug 2022 11:07:58 GMT",
      "difficulty": 2,
      "id": 34,
      "question": "Chelsea football is a Club. In which city is Chelsea located",
      "rating": 4
    }
  ],
  "success": true,
  "total_questions": 1
}
```

#### GET /api/v1/questions

- General:
  - Returns a list of questions objects, categories object, current_category, total_questions and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/questions?page=1`

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "vin"
  },
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
      "rating": 1
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?",
      "rating": 1
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "rating": 4
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?",
      "rating": 1
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?",
      "rating": 3
    },
    {
      "answer": "Brazil",
      "category": 6,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "rating": 1
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?",
      "rating": 1
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?",
      "rating": 1
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?",
      "rating": 1
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?",
      "rating": 1
    }
  ],
  "success": true,
  "total_questions": 22
}
```

#### POST /api/v1/questions

- General:
  - Creates a new question using the submitted question, answer, category, difficulty, and rating.
  - Returns the id of the created question, success value, and a message key.
- Sample: `curl http://127.0.0.1:5000/api/v1/questions/search?page=1 -X POST -H "Content-Type: application/json" -d '{"question":"What is OOP?", "answer":"Object Oriented Programming", "category":1,"difficulty":1, "rating": 2}'`

```bash
{
  "message": "Question created successfully",
  "question_id": 35,
  "success": true
}
```

#### POST /api/v1/questions/search

- General:
  - Returns a list of questions objects, current_category, total_questions and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/v1/questions/search?page=1 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"which"}'`

```bash
{
  "current_category": "Sports",
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "created_at": "Thu, 25 Aug 2022 19:53:31 GMT",
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?",
      "rating": 1
    }
  ],
  "success": true,
  "total_questions": 1
}

```

#### DELETE /api/v1/questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists.
  - Returns the id of the deleted question, success value, and a message key.
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/v1/questions/35`

```bash
{
  "message": "Question deleted successfully",
  "question_id": 35,
  "success": true
}
```

#### POST /api/v1/quizzes

- General:
  - Retrieve a single question for quiz using the submitted quiz_catgeory, and previous_questions.
  - It return a random questions within the given category, if provided, and that is not one of the previous questions
  - So, previous_questions stores questions id's of the previously answered quiz in the specified category
  - Next previous_questions value will be e.g previous_questions:[34]
  - Returns a question object, and success value
- Sample: `curl http://127.0.0.1:5000/api/v1/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":6, "previous_questions":[]}'`

```bash
{
  "question": {
    "answer": "London",
    "category": 6,
    "created_at": "Sat, 27 Aug 2022 11:07:58 GMT",
    "difficulty": 2,
    "id": 34,
    "question": "Chelsea football is a Club. In which city is Chelsea located",
    "rating": 4
  },
  "success": true
}
```

#### GET /api/v1/users

- General:
  - Returns a list of users objects, total_users and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/users?page=1`

```bash
{
  "success": true,
  "total_users": 3,
  "users": [
    {
      "created_at": "Sat, 27 Aug 2022 10:55:30 GMT",
      "fullname": "John Terry",
      "gender": "Male  ",
      "id": 10,
      "username": "terry"
    },
    {
      "created_at": "Sat, 27 Aug 2022 10:55:12 GMT",
      "fullname": "Vincent Ohiri",
      "gender": "Male  ",
      "id": 9,
      "username": "vinnoangel"
    },
    {
      "created_at": "Sat, 27 Aug 2022 10:54:40 GMT",
      "fullname": "jj",
      "gender": "Male  ",
      "id": 8,
      "username": "kkk"
    }
  ]
}
```

#### GET /api/v1/users/{user_id}

- General:
  - Returns a single user object, and success value
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/users/10`

```bash
{
  "success": true,
  "user": {
    "created_at": "Sat, 27 Aug 2022 10:55:30 GMT",
    "fullname": "John Terry",
    "gender": "Male  ",
    "id": 10,
    "username": "terry"
  }
}
```

#### POST /api/v1/users

- General:
  - Creates a new user using the submitted username, fullname, and gender.
  - Returns the id of the created user, success value and a message key
- Sample: `curl http://127.0.0.1:5000/api/v1/users -X POST -H "Content-Type: application/json" -d '{"username":"Emy", "fullname":"Doris", "gender":"Female"}'`

```bash
{
  "message": "User created successfully",
  "user_id": 15,
  "success": true
}
```

#### POST /api/v1/users/search

- General:
  - Returns a list of users objects, total_users and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/api/v1/users/search?page=1 -X POST -H "Content-Type: application/json" -d '{"searchTerm":"terry"}'`

```bash
{
  "success": true,
  "total_users": 1,
  "users": [
    {
      "created_at": "Sat, 27 Aug 2022 10:55:30 GMT",
      "fullname": "John Terry",
      "gender": "Male  ",
      "id": 10,
      "username": "terry"
    }
  ]
}
```

#### DELETE /api/v1/users

- General:
  - Deletes the user of the given ID if it exists.
  - Returns the id of the deleted user, success value, and a message key.
- Sample: `curl -X DELETE http://127.0.0.1:5000/api/v1/users/10`

```bash
{
  "message": "User deleted successfully",
  "user_id": 10,
  "success": true
}
```

#### GET /api/v1/scores

- General:
  - Returns a list of scores objects, total_scoress and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/scores?page=1`

```bash
{
  "scores": [
    {
      "created_at": "Sat, 27 Aug 2022 10:32:19 GMT",
      "expected_score": 2,
      "id": 10,
      "user_id": 1,
      "your_score": 2
    },
    {
      "created_at": "Sat, 27 Aug 2022 10:30:34 GMT",
      "expected_score": 2,
      "id": 9,
      "user_id": 2,
      "your_score": 2
    },
    {
      "created_at": "Sat, 27 Aug 2022 10:18:13 GMT",
      "expected_score": 4,
      "id": 8,
      "user_id": 2,
      "your_score": 2
    }
  ],
  "success": true,
  "total_scores": 3
}
```

#### GET /api/v1/users/{user_id}/scores

- General:
  - Returns a list of scores objects, total_scoress and success value
  - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
- Sample: `curl -X GET http://127.0.0.1:5000/api/v1/users/2/scores?page=1`

```bash
{
  "scores": [
    {
      "created_at": "Sat, 27 Aug 2022 10:30:34 GMT",
      "expected_score": 2,
      "id": 9,
      "user_id": 2,
      "your_score": 2
    },
    {
      "created_at": "Sat, 27 Aug 2022 10:18:13 GMT",
      "expected_score": 4,
      "id": 8,
      "user_id": 2,
      "your_score": 2
    }
  ],
  "success": true,
  "total_scores": 2
}

```

#### POST /api/v1/scores

- General:
  - Upload a new score using the submitted user_id, your_score, and expected_score.
  - This endpoint is for tracking users games. At the end of each quiz, the scores will be recorded
  - Returns the id of the uploaded score, success value and a message key
- Sample: `curl http://127.0.0.1:5000/api/v1/scores -X POST -H "Content-Type: application/json" -d '{"user_id":10, "your_score":3, "expected_score":10}'`

```bash
{
  "message": "Your score has been saved.",
  "user_id": 15,
  "success": true
}
```

## Deployment

Currently, this project isn't hosted yet

## Authors

Vincent Uche Ohiri

My Coach, Ms Caryn at Udacity, Michael my Session Team Lead and many others that time won't permit me mention
