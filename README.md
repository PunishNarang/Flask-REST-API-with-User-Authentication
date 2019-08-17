# Flask REST API with User Authentication

## Installation
1.Flask <br />
2.Flask-JWT <br />
3.Flask-SQLAlchemy<br />
4.Flask-RESTful

```
pip install (All the libraries mentioned in the Installation) 
python app.py (Run app.py on your machine to run the application)
```

## Description

This is a User authenticated REST API implemented using Flask. This API focuses on storing items and store details for a particular user.

For this, first user have to register. After registering , user must login to the to get the authentication key which will be further used to add items/delete items.

After all this work done if user wants to logout of the system, then he can easily logout of the system with all the details saved in the DB for that particular user.

## Implementation

Install Postman on your machine to implement this API.
After installing, use the url on which your application is running (usually 127.0.0.1) in the methods (GET POST DELETE PUT etc) to perform the desired function.

For eg. To register a user---> http://127.0.0.1:(PORT NUMBER)/register

In the Body write the username and password for the user to be registered in the json format.

## Happy Coding!
