# pywochat

## Description

"Pywochat" is the name of the project created as a simple software solution to complete a Python workshop. The main purpose of the application is to talk to any person who has an account created in the application. All you have to do is create your account, log in and start chatting.

## How to run it?

Before you start doing any of the following, make sure you have [PostgreSQL](https://www.postgresql.org/) and [Anaconda](https://www.anaconda.com/) installed on your computer.

### Setting the virtualenv

If you have not already installed **virtualenv** and **pipenv**, do so by opening the Anaconda Prompt and entering the following.

```
$ pip install virtualenv
$ pip install pipenv
```

Navigate to the repository, create and then activate a new virtualenv inside it by entering the following.

```
$ virtualenv pywochat
$ pywochat\Scripts\activate
```

Install the dependencies inside of the newly created virtualenv.

```
$ pipenv install
```

### Setting the database

Open the **pgAdmin** in your browser and create a new database called "**pywochat**". After creating the database, the next step is to create the necessary tables. Run the python interpreter.

```
$ python
```

To create tables from the models defined in app.py, enter the following commands.

```
>>> from app import db
>>> db.create_all()
>>> exit()
```

### And finally, run it!

Navigate to the pywochat, and start the web application by typing the following.

```
$ python app.py
```

## The work is still in progress...

Come and visit us next time.
