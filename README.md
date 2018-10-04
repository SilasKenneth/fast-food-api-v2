### FAST FOOD FAST
Fast-Food-Fast is a food delivery service app for a restaurant. and this is the API(backed) for the app

[![Build Status](https://travis-ci.org/SilasKenneth/fast-food-api-v2.svg?branch=develop)](https://travis-ci.org/SilasKenneth/fast-food-api-v2.svg?branch=develop) 
[![Coverage Status](https://coveralls.io/repos/github/SilasKenneth/fast-food-api-v2/badge.svg?branch=develop)](https://coveralls.io/github/SilasKenneth/fast-food-api-v2?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/c7730ab0e1ca3f6df6fb/maintainability)](https://codeclimate.com/github/SilasKenneth/fast-food-api-v2/maintainability)
## Prerequisites
- [Python3](https://www.python.org/) (A programming language)
- [Flask](http://flask.pocoo.org/) (A Python microframework)
- [PostgreSQL](https://www.postgresql.org/docs/10/static/intro-whatis.html) (Database)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/) (Stores all dependencies used in the project)
- [Pivotal Tracker](www.pivotaltracker.com) (A project management tool)
- [Pytest](https://docs.pytest.org/en/latest/) (Framework for testing)

### Other technologies used:
- Flask_restful
- Postman
- Psycopg2

**The API is hosted [here](https://fastfoodfastapiv2.herokuapp.com)**

### Endpoints

| METHOD | ENDPOINT                                        | DESCRIPTION                      |
| ------ | ---------------------------------------------   | -------------------------------- |
| POST   | '/api/v2/user/signup'                           | User signup               |
| POST   | '/api/v2/user/login '                           | Login signed up user             |
| POST   | '/api/v2/users/orders '                         | Place a new order               |
| GET    | '/api/v2/users/orders/<entry_id>'           | Fetch a specific          |
| GET    | '/api/v2/users/orders'                          | Get all orders for the logged in user              |
| GET   | '/api/v2/orders' | Get all the orders for the admin |
| PUT | '/api/v2/orders/<order_id> | Update the status of an order |
| GET | '/api/v2/menu | Get all menu items |
| GET | '/api/v2/menu/<menu_id>' | Get a given menu item |
| POST | '/api/v2/menu' | Create a new menu item |
| GET | '/api/v2/addresses' | Get all user's addresses |
| POST | 'api/v2/addresses' | Add  an address to the user addresses |

## Getting Started:

**To start this app, please follow the instructions below:**

**On your terminal:**

Install pip:

 `$ sudo apt-get install python-pip`

Clone this repository:

 `$ git clone https://github.com/SilasKenneth/fast-food-api-v2.git`

Get into the root directory:

 `$ cd fast-food-api-v2`

Install virtualenv:

 `$ pip install virtualenv`

Create a virtual environment in the root directory:

 `$ virtualenv name of virtualenv`
  
 Note: If you do not have python3 installed globally, please run this command when creating a virtual environment:
 
 `$ virtualenv -p python3 -name of virtualenv-`

Activate the virtualenv:

 `$ source name of virtualenv/bin/activate`

Install the requirements of the project from the requirements file:

 `$ pip install -r requirements.txt`

Create two databases, one for testing environment and one for development envronnment,as follows:

  `$ createdb fast_food`
  
  `$ createdb testdb`

To run tests:

 `$ pytest`
 
To run the app:

 `$ Python run.py`