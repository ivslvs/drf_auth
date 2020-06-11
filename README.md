Application description

We have two main roles. Clients and Managers.
Clients can register, login by pin code and close their accounts.
Managers are created from admin panel and can approve user
registration and accounts closing.


Clients features

- Clients can register through the POST request to specified
endpoint. Necessary field on registration step: first_name,
last_name, email, passport_number.
After registration account must be in inactive state, until
manager will approve it.

- When account has been accepted, client can enter the profile to
se balance. For this action, client should provide PIN code to
specific endpoint (use whatever method you would like to
provide PIN code)

- Client can close his account in order to leave our system. Then
profile become inactive and waiting for manager to confirm this
action.


Manager features

- Managers are added from admin panel by superadmin

- Managers can go to the special endpoint to see the list of pending
requests for approval, and then approve them one by one

- Managers also have ability to see all closed accounts in order to
confirm the deletion