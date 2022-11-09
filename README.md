# OnBoarding Project

## Introduction

The Goal of this Project is to gain hand on experience of creating scalable web apps which have following features - 

- Restfull API Endpoints
- Test Cases
- Execute Tasks Asynchronously
- Load Testing
- Profiling & Inspection

## Tech Stack

- Python
- Django
- Django Rest Framework
- JWT Authentication
- Pytest
- Locust
- MySQL Database
- Celery & Rabbitmq

## Installation 

- `python3 -m venv yourenvname`
- `source activate yourenvname`
- `git clone https://github.com/subh2310/OnBoard-Project.git
- `pip install -r requirements.txt`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py runserver`

## API Endpoints 

- `/` contains all API Enpoints
- `register/` It is used to register user on the basis of Role that are Merchant and Consumer.
- `login/` It is used to login as Merchant or Consumer.
- `stores/` Merchant can add new and view their registered stores.
- `items/` Merchant can add items under their Registered Stores.
- `place_orders/` It is used by the consumer to place orders.
- `see_orders/` It is used by the merchant to see the orders that have been placed that their registered stores.
- `token/obtain/` It is used by the user to obtain token by providing credentials.
- `token/refresh/` It is used by the user to obtain token by providing refresh token.
- `change-password/` It is used to change the password.
- `view-consumer/` It is used by the merchant to see registered consumer.
- `silk/` It is used for profiling and inspection.


**Note** - Used JWTAuthentication for authenticating the Api Endpoints.
