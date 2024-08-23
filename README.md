# A Dictionary web app

This is a very simple Dictionary which tries to be as customizable as possible

## Requirements

You need python 3.10 and above


## Installation

#### Installing dependencies

I've used poetry as dependency manager.
**If** you have [poetry](https://python-poetry.org/docs/) installed, then you can run the following commands where you colned the repository:
1. `poetry env use python`
2. `poetry shell`
3. `poetry install --no-root`

**Otherwise** you can install dependencies using the *Excellency* `pip` :
1. Firstly it is better to create a virtual environment and activating it:
*CREATE* `python -m venv venv`
*ACTIVATE* `venv/scripts/activate`
2. then:
`pip install -r requirements.txt`


### Migration

After installing the dependencies you **need** to setup your database.
in your activated virtual environment and in the root directory of app run:
`python manage.py migrate`


## Run the app

To run it, *Firstly* activate the virtual environments.
Based on which dependency manager you are using you can activate like this:
1. *Poetry*: `poetry shell`
2. *Pip*: `venv/scripts/activate`

**Then run the app using**: 
`python manage.py runserver 0.0.0.0:8000`


## Using the app

First create a superuser using the following command:
`python manage.py createsuperuser`

then log into the admin panel on `127.0.0.1:8000`
you may start palying by *OriginLanguage* section