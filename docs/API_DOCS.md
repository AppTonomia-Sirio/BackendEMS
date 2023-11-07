# Documentation for the API
# =========================
## Table of Contents

### - [Introduction](#introduction)
### - [Login/Signin](#Login-Signin)
### - [Authentication](#authentication)
### - [Users](#users)
### - [Docs](#docs)

## Introduction
This document describes the API of the project.

## Login-Signin
Users section of API is used for user management. It supports creating, updating, deleting and getting users. 
#### Base URL for users is `/users/`
### Creating a user
To register a user, make a POST request to the `/users/register` endpoint. The request body should contain the following fields:
- email
- password
- name
- surname
- document
- date_of_birth (YYYY-MM-DD)
- home (See [Homes](#homes))
- roles (See [Roles](#roles))

#### request
```
POST /users/register
```

```json
{
    "email": "test@test.com",
    "password": "password",
    "name": "Kurt",
    "surname": "Cobain",
    "document": "13371337L",
    "date_of_birth": "2003-06-30",
    "home": 5,
    "roles": [2,4]
}
```

#### response
```json
{
    "id": 1,
    "email": "test@test.com",
    "name": "Kurt",
    "surname": "Cobain",
    "document": "13371337L",
    "date_of_birth": "2003-06-30",
    "home": 5,
    "roles": [2,4]
}
```

### Logging in
To log in, make a POST request to the `/users/login` endpoint. The request body should contain the following fields:
- email
- password

#### request
```
POST /users/login
```

```json
{
    "email": "test",
    "password": "password"
}
```
#### response
```json
{
  "token": "eyJhbGciOiJIUzI1N..."
}
```
## Authentication
Following endpoints related with user's data require authentication
To authenticate, add the following header to the request:
```
Autorization: Token <token>
```
## Users
Users section of API is used for user management. It supports creating, updating, deleting and getting users.

### Getting a list of users
**You must be authenticated to use this endpoint**
To get a list of users, make a GET request to the `/users/` endpoint.
You can use query parameters to filter the list:
- use `?active=`(`true` or `false`) to filter by activated users
- use `?home=` to filter by name of the user's home
#### request
```
GET /users/
```
#### response
```
[{
  "id": 1,
  "email": "email@test.com"
  ...
}...]
```
### Getting data of current user
**You must be authenticated to use this endpoint**
To get data of current user, make a GET request to the `/users/current` endpoint.
#### request
```
GET /users/current
```
#### response
```
{
  "id": 1,
  "email": "email@test.com"
  ...
}
```
### Updating a user
**You must be authenticated to use this endpoint**
To update a user, make a PUT request to the `/users/<user_id>` endpoint. The request body should contain the following fields:
- email
- password
- name
- surname
- document
- date_of_birth (YYYY-MM-DD)
- home (See [Homes](#homes))
- roles (See [Roles](#roles))

```
PUT /users/<user_id>
```

```
{
    ...
}
```

### Updating a user partially
**You must be authenticated to use this endpoint**
To update a user partially, make a PATCH request to the `/users/<user_id>` endpoint. The request body should contain only the fields that are to be updated.
```
PATCH /users/<user_id>
```

```json
{
    "surname": "Vonegut"
}
```

### Retrieving a user
**You must be authenticated to use this endpoint**
To retrieve a user, make a GET request to the `/users/<user_id>` endpoint.
#### request
```
GET /users/<user_id>
```
#### response
```
{
  ...
}
```

### Changing status of a user
**You must be authenticated to use this endpoint**
**You must be an admin or superuser to use this endpoint**
To change status of a user, make a PUT request to the `/users/<user_id>/status` endpoint. The request body should contain the following fields:
- status ('Active', 'Pending' or 'Frozen')
#### request
```
PUT /users/<user_id>/status
```

```json
{
    "status": "Active"
}
```
#### response
```
{
  'status': 'Active'
}
```

### Homes 

#### Retrieving a list of homes
To retrieve a list of homes, make a GET request to the `users/homes/` endpoint.
#### request
```
GET users/homes/
```
#### response
```
[
  {
    "id": 1,
    "name": "Home 1",
    "address": "Address 1"
  },
  {
    "id": 2,
    "name": "Home 2",
    "address": "Address 2"
  }
]
```
#### Retrieving a home
To retrieve a home, make a GET request to the `users/homes/<home_id>` endpoint.
#### request
```
GET users/homes/<home_id>
```
#### response
```
{
  "id": 1,
  "name": "Home 1",
  "address": "Address 1"
}
```
### Roles
#### Retrieving a list of roles
To retrieve a list of roles, make a GET request to the `users/roles/` endpoint.
#### request
```
GET users/roles/
```
#### response
```
[
  {
    "id": 1,
    "name": "Role 1"
  },
  {
    "id": 2,
    "name": "Role 2"
  }
]
```
#### Retrieving a role
To retrieve a role, make a GET request to the `users/roles/<role_id>` endpoint.
#### request
```
GET users/roles/<role_id>
```
#### response
```
{
  "id": 1,
  "name": "Role 1"
}
```
## Docs
The API supports getting list of docs. To get the list of autodocs made with coreAPI, make a GET request to the `/docs/` endpoint.
```
GET /docs/
```




