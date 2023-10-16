# pywochat

[![Build Status](https://app.travis-ci.com/corlukantonio/pywochat.svg?branch=master)](https://app.travis-ci.com/corlukantonio/pywochat)

## Description

**Pywochat** is the name of the project created as a simple software solution for the completion of the Python workshop held in the premises of the Faculty of Organization and Informatics in Varaždin. The main purpose of the application is to enable a conversation through a simple interface with any person who has created an account within the application. All you have to do is create your account, log in and start chatting.

## Setting WSL and Docker

## How to run it?

Before you start doing any of the following, make sure you have [PostgreSQL](https://www.postgresql.org/) and [Anaconda](https://www.anaconda.com/) installed on your computer.

One important change to make within the [app.py](https://github.com/corlukantonio/pywochat/blob/master/app.py) document, if you are going to run it on localhost, is to change the ENV variable.

```python
# If running on localhost set this to 'dev'
ENV = 'prod'
```

### Setting the virtualenv

If you have not already installed **virtualenv** and **pipenv**, do so by opening the Anaconda Prompt and entering the following.

```properties
pip install virtualenv
pip install pipenv
```

Navigate to the repository, create and then activate a new virtualenv inside it by entering the following.

```properties
virtualenv pywochat
pywochat\Scripts\activate
```

Install the dependencies inside of the newly created virtualenv.

```properties
pipenv install
```

### Setting the database

Open the **pgAdmin** in your browser and create a new database called "**pywochat**". After creating the database, the next step is to create the necessary tables. Run the python interpreter.

```properties
python
```

To create tables from the models defined in app.py, enter the following commands.

```python
from app import db
db.create_all()
exit()
```

### And finally, run it!

Navigate to the pywochat, and start the web application by typing the following.

```properties
python app.py
```

## The work is still in progress...

Come and visit us next time.
