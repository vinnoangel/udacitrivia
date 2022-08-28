# Udacitrivia Backend API

All backend code follows [PEP8 Style Guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Pre-requisites and Local Development

To get started with this application, you must have python3, pip, postgresql and node installed

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

## Authors

Vincent Uche Ohiri

My Coach, Ms Caryn at Udacity, Michael my Session Team Lead and many others that time won't permit me to mention
