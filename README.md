# pywochat

[![Python CI](https://github.com/corlukantonio/pywochat/actions/workflows/ci.yml/badge.svg)](https://github.com/corlukantonio/pywochat/actions/workflows/ci.yml)
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
        <td>10.0.19045.5917</td>
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
docker run -p 5433:5432 \
  -e POSTGRES_USER=pywochat_user \
  -e POSTGRES_PASSWORD=123456 \
  -e POSTGRES_DB=pywochat \
  -d postgres
```

## Environment variables

The environment variables required for this application are listed and described below.

<table align="center">
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>PYWOCHAT_DATABASE_URI</td>
      <td>Database URI.</td>
    </tr>
    <tr>
      <td>PYWOCHAT_SECRET_KEY</td>
      <td>Secret key.</td>
    </tr>
  </tbody>
</table>

## How to run it?

Before you start doing any of the following, make sure you have [PostgreSQL](https://www.postgresql.org/) and [Anaconda](https://www.anaconda.com/) installed on your computer.

### Setting the virtualenv

If you have not already installed **virtualenv**, do so by opening the Anaconda Prompt and entering the following.

```properties
pip install virtualenv
```

Navigate to the repository, create and then activate a new virtualenv inside it by entering the following.

```properties
virtualenv pywochatenv --python=python3.13
```

```properties
source pywochatenv/Scripts/activate
```

Install the dependencies inside of the newly created virtualenv.

```properties
pip install -r requirements.txt
```

### Setting the database

To create the database and tables (from the migrations), enter the following command.

```properties
flask db upgrade
```

### And finally, run it!

Navigate to the pywochat, and start the web application by typing the following.

```properties
python run.py
```
