# pywochat

[![Build Status](https://app.travis-ci.com/corlukantonio/pywochat.svg?branch=master)](https://app.travis-ci.com/corlukantonio/pywochat)

## Description

**Pywochat** is the name of the project created as a simple software solution for the completion of the Python workshop held in the premises of the Faculty of Organization and Informatics in Varaždin. The main purpose of the application is to enable a conversation through a simple interface with any person who has created an account within the application. All you have to do is create your account, log in and start chatting.

## Setting WSL and Docker

### WSL

Assuming WSL is already setup, below is information about WSL and the Linux distro used for development.

```properties
wsl --version
```

<details>
  <summary>Output</summary>
  <table align="center">
    <thead>
      <tr>
        <th>Parameter</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>WSL version</td>
        <td>2.0.14.0</td>
      </tr>
      <tr>
        <td>Kernel version</td>
        <td>5.15.133.1-1</td>
      </tr>
      <tr>
        <td>WSLg version</td>
        <td>1.0.59</td>
      </tr>
      <tr>
        <td>MSRDC version</td>
        <td>1.2.4677</td>
      </tr>
      <tr>
        <td>Direct3D version</td>
        <td>1.611.1-81528511</td>
      </tr>
      <tr>
        <td>DXCore version</td>
        <td>10.0.25131.1002-220531-1700.rs-onecore-base2-hyp</td>
      </tr>
      <tr>
        <td>Windows version</td>
        <td>10.0.19045.5073</td>
      </tr>
    </tbody>
  </table>
</details>

```properties
cat /etc/os-release
```

<details>
  <summary>Output</summary>
  <table align="center">
    <thead>
      <tr>
        <th>Key</th>
        <th>Value</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>PRETTY_NAME</td>
        <td>"Debian GNU/Linux 12 (bookworm)"</td>
      </tr>
      <tr>
        <td>NAME</td>
        <td>"Debian GNU/Linux"</td>
      </tr>
      <tr>
        <td>VERSION_ID</td>
        <td>"12"</td>
      </tr>
      <tr>
        <td>VERSION</td>
        <td>"12 (bookworm)"</td>
      </tr>
      <tr>
        <td>VERSION_CODENAME</td>
        <td>bookworm</td>
      </tr>
      <tr>
        <td>ID</td>
        <td>debian</td>
      </tr>
      <tr>
        <td>HOME_URL</td>
        <td>"https://www.debian.org/"</td>
      </tr>
      <tr>
        <td>SUPPORT_URL</td>
        <td>"https://www.debian.org/support"</td>
      </tr>
      <tr>
        <td>BUG_REPORT_URL</td>
        <td>"https://bugs.debian.org/"</td>
      </tr>
    </tbody>
  </table>
</details>

### Docker

Following the [installation instructions](https://docs.docker.com/engine/install/debian/) for Debian you should have Docker set up and ready to run the containers needed for development. Now to provide the infrastructure for the application, start the docker container by executing the command below.

```properties
docker run -e POSTGRES_PASSWORD=123456 -d postgres
```

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
```

```properties
pip install pipenv
```

Navigate to the repository, create and then activate a new virtualenv inside it by entering the following.

```properties
virtualenv pywochat --python=python3.11
```

```properties
source pywochat/Scripts/activate
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
```

```python
with app.app_context():
  db.create_all()
```

```python
exit()
```

### And finally, run it!

Navigate to the pywochat, and start the web application by typing the following.

```properties
python app.py
```

## The work is still in progress...

Come and visit us next time.
