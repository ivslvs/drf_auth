This application is written in Python using Django REST framework.


# Application description:

We have two main roles. Clients and Managers.
Clients can register, login and close their accounts.
Managers are created from admin panel and can approve user
registration and accounts closing.


## Clients features

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


## Manager features

- Managers are added from admin panel by superadmin

- Managers can go to the special endpoint to see the list of pending
requests for approval, and then approve them one by one

- Managers also have ability to see all closed accounts in order to
confirm the deletion


# Installing:

pipenv install

pipenv shell

pipenv install --dev

python manage.py runserver



You can use swagger or routes below

# The routes:

#### User's registration, login, logout:

- POST /register/ - User's endpoint for registration

Exp body: {"username": "testuser", "email": "testuser@email.com", "first_name": "testuser", "last_name": "testuser", "passport_number": "546fgh", "password": "testuser"}

- POST /rest-auth/login/ - User's login

Exp body: {"username": "testuser", "email": "testuser@email.com", "password": "testuser"}

- POST /rest-auth/logout/ - Calls Django logout method and delete the Token object assigned to the current User objectexp.

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

#### Managers' routes:

- GET /api/v1/managers/activation_deactivation/?status=RA - Manager's endpoint to see the clients list for activation

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

- GET /api/v1/managers/activation_deactivation/?status=RD - Manager's endpoint to see the clients list for deactivation

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

- GET /api/v1/managers/activation_deactivation/?status=A - Manager's endpoint to see activated clients list

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

- GET /api/v1/managers/activation_deactivation/?status=D - Manager's endpoint to see deactivated clients list

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

- PUT /api/v1/managers/activation/{id}/ - Manager's endpoint for client activation

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

- PUT /api/v1/managers/deactivation/{id}/ - Manager's endpoint for client deactivation

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

#### Clients' routes:

- GET /api/v1/clients/balance/{id}/ - Client's endpoint to see balance

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17

- PUT /api/v1/clients/deletion/{id}/ - Client's endpoint to leave the system

Exp body: {"email": "testuser@email.com"}

Exp Headers: Token de1d046282563426b00aae569b1c58de6d8c7f17
