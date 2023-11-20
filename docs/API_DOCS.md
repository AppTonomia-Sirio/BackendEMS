# Documentation for the API
# =========================

## [Authentication](#authentication)
#### - [Signing up](#signing-up)
#### - [Logging in](#logging-in)
#### - [Token management](#token-management)
## [Users](#users)
#### - [Getting data of the current user](#getting-data-of-the-current-user)
#### - [Getting list of users](#getting-list-of-users)
- [Filtering](#filtering)
#### - [Getting user details](#getting-user-details)
#### - [Updating user details](#updating-user-details)
#### - [Partially updating user details](#partially-updating-user-details)
#### - [Changing user status](#changing-user-status)
#### - [Deleting user](#deleting-user)
## [Homes and roles](#homes-and-roles)
#### - [Getting list of homes](#getting-list-of-homes)
#### - [Getting home details](#getting-home-details)
#### - [Getting list of roles](#getting-list-of-roles)
#### - [Getting role details](#getting-role-details)

## Authentication
To use the majority of the API endpoints, you need to be authenticated.
### Signing up
Let's first create a new user. To do that, we need to send a `POST` request to `/users/register/` with the following data:
```json
{
    "email": "...",
    "name": "...",	
    "surname": "...",
    "password": "...",
    "document": "...",
    "date_of_birth": "...",
    "home": "...",
    "roles": ["..."]
}
```
The `home` field is the ID of the home the user is going to be assigned to.

The `roles` field is a list of IDs of roles the user is going to be assigned to.

The `date_of_birth` field is a string in the format `YYYY-MM-DD`.

The `document` field is a string containing the document number of the user.

The `password` field is a string containing the password of the user.

The `email` field is a string containing the email of the user.

The `name` field is a string containing the name of the user. 

The `surname` field is a string containing the surname of the user.

The response will be:
```json
{
    "id": "...",
    "email": "...",
    "name": "...",
    "surname": "...",
    "document": "...",
    "date_of_birth": "...",
    "home": "...",
    "roles": ["..."]
}
```
##








