# Project README

## Frameworks Available
- Django
- Flask
- FastAPI

## Framework Chosen
FastAPI

## Why FastAPI is Chosen Over the Rest
FastAPI was selected due to its asynchronous support, automatic data validation using Python type hints, and seamless integration with OpenAPI and JSON Schema documentation. It provides efficient API development with minimal boilerplate code, making it an excellent choice for this project.

## Choice of Database
MongoDB

## Searching Text
For searching keywords I created a $text index on both body and title

## How to Run the App
Run the following command in the terminal:
```bash
make server
```
As an alternative you can also execute run.sh in a docker container and make requests from Postman

## Unit Tests
Unit tests were initially implemented using mock function calls. However, they became too lengthy, leading to a shift in focus towards authentication. 

## Authentication
Authentication is implemented using both JWT and PASETO (A much better alternative to JWT), One of it's requirements libsodium which does not run properly on mac so deployed it on Docker Container (Linux Os, Python Image)

## Docker
The application successfully runs on Docker using an Ubuntu image.

## Architecture
The project adheres to the standard MVC (Model-View-Controller) architecture, ensuring clean and tidy code organization.
