 This application is written in Python using Django REST framework.
- Python 3.8
- Django REST Framework
- PostgreSQL
- Docker


# Application description

We have two main roles. Clients and Managers.
Clients can register, login and close their accounts.
Managers are created from admin panel and can approve user
registration and accounts closing.


## Implemented Clients features

- Clients can register through the POST request to specified
endpoint. Necessary field on registration step: first_name,
last_name, email, passport_number.
After registration account must be in inactive state, until
manager will approve it.

- When account has been accepted, client can enter the profile to
se balance.

- Client can close his account in order to leave our system. Then
profile become inactive and waiting for manager to confirm this
action.


## Implemented Managers features

- Managers are added from admin panel by superadmin

- Managers can go to the special endpoint to see the list of pending
requests for approval, and then approve them one by one

- Managers also have ability to see all closed accounts in order to
confirm the deletion


# Quick start
```sh
docker-compose build
docker-compose run web python manage.py migrate
docker-compose run web python manage.py createsuperuser
docker-compose up

docker-compose down

```

# API Documentation

[Detailed API documentation](https://documenter.getpostman.com/view/8690633/TVKJyuuF#abe89677-bccd-468a-995f-ea63505f8b1c) generated by Postman
