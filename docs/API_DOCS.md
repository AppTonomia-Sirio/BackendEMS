# Documentation for the API <!-- omit in toc -->

- [Authentication](#authentication)
  - [Sign Up](#sign-up)
    - [Signing up as an NNA](#signing-up-as-an-nna)
    - [Signing up as a Staff user](#signing-up-as-a-staff-user)
  - [Logging in](#logging-in)
  - [Token management](#token-management)
- [Users](#users)
  - [Getting list of NNAs](#getting-list-of-nnas)
    - [Filtering NNA](#filtering-nna)
  - [Getting list of Staff](#getting-list-of-staff)
    - [Filtering Staff](#filtering-staff)
  - [NNA operations](#nna-operations)
    - [Getting NNA details](#getting-nna-details)
    - [Updating NNA details](#updating-nna-details)
    - [Partially updating NNA details](#partially-updating-nna-details)
    - [Deleting NNA](#deleting-nna)
  - [Staff operations](#staff-operations)
    - [Getting Staff details](#getting-staff-details)
    - [Updating Staff details](#updating-staff-details)
    - [Partially updating Staff details](#partially-updating-staff-details)
    - [Deleting NNA](#deleting-nna-1)
- [Homes and roles](#homes-and-roles)
  - [Getting list of homes](#getting-list-of-homes)
  - [Getting home details](#getting-home-details)
  - [Getting list of roles](#getting-list-of-roles)
  - [Getting role details](#getting-role-details)
- [Not found](#not-found)


# Authentication
To use the majority of the API endpoints, you need to be authenticated.
## Sign Up
### Signing up as an NNA
Let's create a new NNA user. To do that, we need to send a `POST` request to `/users/nna/` with the following data:
```json
{
    "email": "...",
    "name": "...",	
    "surname": "...",
    "password": "...",
    "document": "...",
    "date_of_birth": "...",
    "home": "...",
    "gender": "..."
}
```
The `gender` field is the gender of the NNA, it can take the following values `{Male, Female, Other, Undefined}` default is `Undefined`. It is optional.

The `home` field is the ID of the home the user is going to be assigned to.

The `date_of_birth` field is a string in the format `YYYY-MM-DD`.

The `document` field is a string containing the document number of the user. It is optional.

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
    "created_at": "...",
    "document": "...",
    "date_of_birth": "...",
    "home": "...",
    "status": "Pending",
    "gender": "...",
    "mentors": [],
    "therapist": null,
    "autonomy_level": 1,
    "tutor": null,
    "entered_at": null
}
```
### Signing up as a Staff user
Let's create a new Staff user. To do that, we need to send a `POST` request to `/users/staff/` with the following data:
```json
{
    "email": "...",
    "name": "...",	
    "surname": "...",
    "password": "...",
    "homes":["..."],
    "roles":["..."],
    "is_admin":"..."
}
```
The `is_admin` field is a boolean determining the admin status of the user.

The `roles` field is an array of the IDs of the roles this user is going to be asigned to.

The `homes` field is an array of the IDs of the homes the user is going to be assigned to.

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
    "created_at": "...",
    "homes":["..."],
    "roles":["..."],
    "is_admin":"..."
}
```
## Logging in
To log in, we need to send a `POST` request to `/users/login/` with the following data:
```json
{
    "email": "...",
    "password": "..."
}
```
The `email` field is a string containing the email of the user.
The `password` field is a string containing the password of the user.

The response will be:
```json
{
    "token": "..."
}
```

## Token management
To use the majority of the API endpoints, you need to be authenticated. To do that, you need to send the token in the `Authorization` header of the request. The token is returned when you log in. The header should look like this:
```
[
    "Authorization": "Token <token>"
]
```

# Users
## Getting list of NNAs
To get the list of NNAs, we need to send a `GET` request to `/users/nna/`. The response will be:
```json
[
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "document": "...",
        "date_of_birth": "...",
        "home": "...",
        "status": "...",
        "gender": "...",
        "mentors": ["..."],
        "therapist": "...",
        "autonomy_level": "...",
        "tutor": "...",
        "entered_at": "..."
    },
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "document": "...",
        "date_of_birth": "...",
        "home": "...",
        "status": "...",
        "gender": "...",
        "mentors": ["..."],
        "therapist": "...",
        "autonomy_level": "...",
        "tutor": "...",
        "entered_at": "..."
    },
  ...
]
```
### Filtering NNA
You can filter the list of NNAs by sending a `GET` request to `/users/nna/?<filter>=<value>`. The response will be:
```json
[
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "document": "...",
        "date_of_birth": "...",
        "home": "...",
        "status": "...",
        "gender": "...",
        "mentors": ["..."],
        "therapist": "...",
        "autonomy_level": "...",
        "tutor": "...",
        "entered_at": "..."
    },
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "document": "...",
        "date_of_birth": "...",
        "home": "...",
        "status": "...",
        "gender": "...",
        "mentors": ["..."],
        "therapist": "...",
        "autonomy_level": "...",
        "tutor": "...",
        "entered_at": "..."
    },
  ...
]
```
The available filters are:
```py
"id",
"email",
"name",
"surname",
"created_at",
"document",
"date_of_birth",
"home",
"status",
"gender",
"mentors",
"therapist",
"autonomy_level",
"tutor",
"entered_at"
```

## Getting list of Staff
To get the list of Staff, we need to send a `GET` request to `/users/staff/`. The response will be:
```json
[
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "homes":["..."],
        "roles":["..."],
        "is_admin":"..."
    },
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "homes":["..."],
        "roles":["..."],
        "is_admin":"..."
    },
  ...
]
```
### Filtering Staff
You can filter the list of NNAs by sending a `GET` request to `/users/staff/?<filter>=<value>`. The response will be:
```json
[
        {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "homes":["..."],
        "roles":["..."],
        "is_admin":"..."
    },
    {
        "id": "...",
        "email": "...",
        "name": "...",
        "surname": "...",
        "created_at": "...",
        "homes":["..."],
        "roles":["..."],
        "is_admin":"..."
    },
  ...
]
```
The available filters are:
```py
"id",
"email",
"name",
"surname",
"created_at",
"homes",
"roles",
"is_admin"
```
## NNA operations
### Getting NNA details
To get the details of a user, we need to send a `GET` request to `/users/nna/<id>/`. The response will be:
```json
{
    "id": "...",
    "email": "...",
    "name": "...",
    "surname": "...",
    "created_at": "...",
    "document": "...",
    "date_of_birth": "...",
    "home": "...",
    "status": "...",
    "gender": "...",
    "mentors": ["..."],
    "therapist": "...",
    "autonomy_level": "...",
    "tutor": "...",
    "entered_at": "..."
}
```
### Updating NNA details
To update the details of a user, we need to send a `PUT` request to `/users/nna/<id>/` with the following data:
```json
{
    "email": "...",
    "name": "...",
    "surname": "...",
    "document": "...",
    "date_of_birth": "...",
    "home": "...",
    "status": "...",
    "gender": "...",
    "mentors": ["..."],
    "therapist": "...",
    "autonomy_level": "...",
    "tutor": "...",
    "entered_at": "..."
}
```

### Partially updating NNA details
To partially update the details of a user, we need to send a `PATCH` request to `/users/nna/<id>/` with the following data:
```json
{
    "field_to_update": "...",
    ...
}
```

### Deleting NNA
To delete a user, we need to send a `DELETE` request to `/users/nna/<id>/`.
You can only delete a user being a superuser.

## Staff operations
### Getting Staff details
To get the details of a user, we need to send a `GET` request to `/users/staff/<id>/`. The response will be:
```json
{
    "id": "...",
    "email": "...",
    "name": "...",
    "surname": "...",
    "created_at": "...",
    "homes":["..."],
    "roles":["..."],
    "is_admin":"..."
}
```
### Updating Staff details
To update the details of a user, we need to send a `PUT` request to `/users/staff/<id>/` with the following data:
```json
{
    "id": "...",
    "email": "...",
    "name": "...",
    "surname": "...",
    "created_at": "...",
    "homes":["..."],
    "roles":["..."],
    "is_admin":"..."
}
```

### Partially updating Staff details
To partially update the details of a user, we need to send a `PATCH` request to `/users/staff/<id>/` with the following data:
```json
{
    "field_to_update": "...",
    ...
}
```

### Deleting NNA
To delete a user, we need to send a `DELETE` request to `/users/staff/<id>/`.
You can only delete a user being a superuser.

# Homes and roles
## Getting list of homes
To get the list of homes, we need to send a `GET` request to `users/homes/`. The response will be:
```json
[
    {
        "id": "...",
        "name": "...",
        "address": "..."
    },
    {
        "id": "...",
        "name": "...",
        "address": "..."
    },
  ...
]
```
## Getting home details
To get the details of a home, we need to send a `GET` request to `users/homes/<id>/`. The response will be:
```json
{
    "id": "...",
    "name": "...",
    "address": "..."
}
```
## Getting list of roles
To get the list of roles, we need to send a `GET` request to `users/roles/`. The response will be:
```json
[
    {
        "id": "...",
        "name": "..."
    },
    {
        "id": "...",
        "name": "..."
    },
  ...
]
```
## Getting role details
To get the details of a role, we need to send a `GET` request to `users/roles/<id>/`. The response will be:
```json
{
    "id": "...",
    "name": "..."
}
```

# Not found
If you try to access an endpoint that doesn't exist, you will get a `404` response with the following data:
```json
{
    "error": "Not found"
}
```








