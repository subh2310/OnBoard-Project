# Updated-Onboarding
## Food Hub
 A Django Application to perform CRUD Operations on Entities such as Merchant, Item, Store, Order.

## Motivation
Idea is to gain a understanding of how Django and relevant frameworks such as Django Rest Framework, pytest etc work with an emphasis on producing scalable and maintainable code.

## Tech/Framework used

- Django 
- MySql 
- Django Rest Framework
- pytest-django 
- django-silk  
- Celery
- Rabbitmq
- JWT Authentication
- Structlog

## Features
- Add/view(list, detail)/update/delete entries for Merchant, Item, Store and Orders.
- See list of stores/items/orders belonging to a Merchant.
- See list of Orders placed for a particular store. 


## Getting the Application up and running. 
- git clone https://github.com/subh2310/OnBoard-Project.git
- virtualenv env --> To create virtualenv
- source env/bin/activate --> To activate virtual environment in which all the project dependencies will be installed.
- Navigate to Directory containing requirements.txt 
- pip3 install -r requirements.txt --> Install project dependencies
- python3 manage.py migrate  --> To apply migrations in Local Database. 
- python manage.py collectstatic --> To collect static files from multiple apps into a single path
- python3 manage.py runserver --> To start server


## Testing - Setup and Execution 
- Navigating to Directory containing requirements.txt.
- pip3 install -r requirements.txt -> Install Dependencies for Testing
- Run command: pytest -> to execute the tests.

