pipenv shell

pipenv install --dev

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser --email admin@email.com --first_name admin --last_name admin --passport_number 123qwert



1) 'http://127.0.0.1:8000/api/accounts/register/' - регистрация
2) 'http://127.0.0.1:8000/api/accounts/activation/' - список ссылок на активацию клиента (менеджера я не реализовала, поэтому доступ без токена и пермишенс)
3) 'http://127.0.0.1:8000/api/accounts/login/' - клиент логинится
4) 'http://127.0.0.1:8000/api/accounts/balance/'pk/ - клиент может посмотреть свой баланс
5) 'http://127.0.0.1:8000/api/accounts/logout/'pk/ - лог аут клиента
6) 'http://127.0.0.1:8000/api/accounts/deactivation/' - список ссылок на деактивацию клиентов (менеджера я не реализовала, поэтому доступ без токена и пермишенс)

РЕАЛИЗОВАЛА:

Clients features:
- Clients can register through the POST request to specified
endpoint. Necessary field on registration step: first_name,
last_name, email, passport_number.
After registration account must be in inactive state, until
manager will approve it.

- When account has been accepted, client can enter the profile to
se balance. For this action, client should provide PIN code to
specific endpoint (use whatever method you would like to
provide PIN code)

Менеджер подтверждает активацию клиента, клиент логиниться в системе (email, password по token auth), 
после у клиента есть возможность смотреть свой баланс

- Client can close his account in order to leave our system. Then
profile become inactive and waiting for manager to confirm this
action.

Клиент выходит из системы (log out), Менеджер подтверждает деактивацию клиента


Manager features:

- Managers can go to the special endpoint to see the list of pending
requests for approval, and then approve them one by one

- Managers also have ability to see all closed accounts in order to
confirm the deletion

НЕ РЕАЛИЗОВАЛА:
- Managers are added from admin panel by superadmin

После переопределения своей модели Client, в админке в регистрации пропало поле где я выбирала группу с пермишенс
Т.е. я могу создать группу "Managers", но не могу добавить туда юзеров тк такого поля просто нет

у меня есть 2 варианта как это сделать:

-переопределить модеть Group (в своем коде я это сделала, но оно не работает и выглядит неоч)

-прикрутить встроенную модель Group в регистрацию (как в классическом варианте админки) - мне этот вариант нравится

как сделать эти 2 варианта - не знаю 



В некоторых файлах у меня написаны вопросы к тебе:

tests.py - 2 вопроса

views.py - 2 вопроса




По возможности:

-ответь плес на вопросы в файлах

-как лучше реализовать Менеджеров

-скажи свое мнение о моем коде, что хорошо\плохо\можно поменять\улучшить

-насколько чисто и читаемо написано

-мною написанные тесты меня не успокаивают. как много их нужно писать?
