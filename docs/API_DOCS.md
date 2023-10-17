# Documentation for the API
# =========================
#
## Table of Contents
#
# - [Introduction](#introduction)
# - [Authentication](#authentication)
# - [Creating users](#users)
# - [List of locations](#locations)
# - [List of therapists](#therapists)
# - [Docs](#docs)

## Introduction
This document describes the API of the project.

## Authentication
The API uses token authentication. To authenticate, make a POST request to the `/login/` endpoint with the user's credentials. If the credentials are valid, the server will return a JSON response with the access token and status code 200, otherwise it will return a JSON response with an error message and status code 400.

### Example
#### Request
```
POST /login/
```
```json
{
    "email": "email",
    "password": "password"
}
```
#### Response
```json
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### How to authenticate?

Get the token from the response of `/login/` endpoint and add it to the header of the request.

## Getting status of NNA user

The API supports getting status of NNA user. To get the status of NNA user, make a GET request to the `/status/` endpoint.
### **<u>You must be authenticated and also be NNA user</u>!**

### Example

#### Request
```
GET /status/
```
```
Headers = [
    ...
    Authorization: Token YOUR_TOKEN
    ...
]
```
#### Response
```json
{
    "status": "A"
}
```

## Users
For the moment, the API only supports creating 'NNA' users. To create a 'NNA' user, make a POST request to the `/register/` endpoint with the user's data.

If the credentials are valid, the server will return a JSON response with user's data.
#### fields:
- `email` (string) (unique)
- `password` (string)
- `name` (string)
- `surname` (string)
- `location` (int) (pk of the location, see [Locations](#locations))
- `date_of_birth` (date) (format: YYYY-MM-DD)
- `mentor` (int) (pk of the mentor, see [Therapists](#therapists))
#### All fields are required.
### Example
#### Request
```
POST /register/
```
```json
{
    "email": "example@example.com",
    "password": "password",
    "name": "John",
    "surname": "Doe",
    "location": 1,
    "date_of_birth": "1990-01-01",
    "mentor": 1
}
```
#### Response
```json
{
    "email": "example@example.com",
    "name": "John",
    "surname": "Doe",
    "location": 1,
    "date_of_birth": "1990-01-01",
    "mentor": 1,
    "id": 1,
    "status": "A"
}
```
## Getting user data
The API supports getting the data of an user. To get the data of an user make a GET request to the `/user/<str:email>/` endpoint where `<str:email>` is the email of the desired user.
### **<u>You must be authenticated and also be NNA user</u>!**
### Example
#### Request
```
GET /user/example@example.com/
```
```
Headers = [
    ...
    Authorization: <Token YOUR_TOKEN>
    ...
]
```
#### Response
```json
{
    "email": "example@example.com",
    "name": "John",
    "surname": "Doe",
    "location": 1,
    "date_of_birth": "1990-01-01",
    "mentor": 2,
    "status": "A",
    "id": 3
}
```
## Locations
The API supports getting list of locations. To get the list of locations, make a GET request to the `/locations/` endpoint. 
### Example
#### Request
```
GET /locations/
```
#### Response
```json
[
    {
        "id": 1,
        "name": "Location 1"
    },
    {
        "id": 2,
        "name": "Location 2"
    }
]
```
## Therapists
The API supports getting list of therapists. To get the list of therapists, make a GET request to the `/therapists/` endpoint.
### Example
#### Request
```
GET /therapists/
```
#### Response
```json
[
    {
        "email": "example1@gmail.com",
        "name": "John",
        "surname": "Doe",
        "id": 1
    },
    {
        "email": "example2@gmail.com",
        "name": "Marry",
        "surname": "Smith",
        "id": 2
    }
    
]
```
## NNAs assigned to therapist
The API supports getting a list of all NNAs assigned to a therapist. To get the list, you must be authenticated as a therapist, make a get GET request to the `/therapist-nna/` endpoint.
### **<u>You must be authenticated and also be NNA user</u>!**
### Example
```
GET /therapist-nna/
```
```
Headers = [
    ...
    Authorization: <Token YOUR_TOKEN>
    ...
]
```
#### Response
```json
[
    {
        "email": "example@example.com",
        "name": "John",
        "surname": "Doe",
        "location": 1,
        "date_of_birth": "1990-01-01",
        "mentor": 2,
        "status": "A",
        "id": 3
    },
    {
        "email": "example2@example.com",
        "name": "Marie",
        "surname": "Doe",
        "location": 1,
        "date_of_birth": "1990-01-01",
        "mentor": 2,
        "status": "A",
        "id": 4
    }
]
```
## Docs
The API supports getting list of docs. To get the list of autodocs made with coreAPI, make a GET request to the `/docs/` endpoint.
```
GET /docs/
```




