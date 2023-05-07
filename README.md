[![Django Version](https://img.shields.io/badge/django-4.2-green.svg)](https://docs.djangoproject.com/en/3.2/)
[![Django REST framework](https://img.shields.io/badge/django--rest--framework-3.14-green.svg)](https://www.django-rest-framework.org/)
[![pytest](https://img.shields.io/badge/pytest-7.3.1-green.svg)](https://docs.pytest.org/en/stable/)
[![Python Version](https://img.shields.io/badge/python-3.9.7-blue.svg)](https://www.python.org/downloads/release/python-390/)


# ice-cream-shop

A project to automate icecream orders. A user can order several scoops of different ice cream flavor and an admin can manage ice cream tubs stock.

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PYTHONPATH=/{YOUR_PATH_TO_PROJECT}/nalo-test/
icecreamshop`

`DJANGO_SETTING_MODULE=icecreamshop.settings`



## Run Locally

Clone the project

```bash
  git clone https://github.com/MrBloon/nalo-test.git
```

Install pipenv and activate the virtualvenv

```bash
  pip install pipenv
  pipenv shell
```

Go to the project directory

```bash
  cd nalo-test
```

Install dependencies

```bash
  pipenv install
```

Create flavors and stocks

```bash
  cd icecreamshop
  bash scripts/create_db_test.sh
```


Start the Django server

```bash
  python manage.py runserver
```

## Running Tests

To run tests, run the following command

```bash
  pipenv run pytest .
```

## Admin back office

To go to the back office, start the Django server and go to:
`http://localhost:8000/admin`

Enter the username and password:
`nalo_admin`
`nalo2023`

If module tzdata is not found, install it:
```bash
  pipenv install tzdata
```
