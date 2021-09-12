# user-auth-restful-interface
A RESTful interface offering cookie-based user authentication using the Argon2 cryptographic hashing function to hash and store passwords in a MySQL database. Uses an object relational mapping (ORM) to manage interactions with the database and is written using Flask.

The interface supports three endpoints: registrations, sessions, and logged_in. Registrations can be used to create user accounts, sessions can be used to log users in and out, and logged_in can be used to check whether or not a user is currently logged in.

During user registration, the interface enforces a number of restrictions having to do with the validity of certain usernames and passwords, including that: (1) usernames must not already be registered with the server, (2) usernames must not be empty or all white-space, (3) usernames must be between 8 and 20 characters long, (4) passwords must not be empty or all white-space, and (5) passwords must be at least 8 characters long.

## Creating an account - POST on '/auth/registrations'
| Method | Request Body | Response Body | Status Code
| --- | --- | --- | --- |
| POST | {<br />  "username": "exampleusername",<br/> "password": "examplepassword"<br/>} | {<br/> "status": "created",<br/> "logged_in": true,<br/>"user": {<br/>"id": unique integer id,<br/>"username": "exampleusername"<br/>}<br/>} | 200 |
| POST | {<br />  "username": "takenusername",<br/> "password": "examplepassword"<br/>} | "Username takenusername taken." | 400 |
| POST | {<br />  "username": "",<br/> "password": "examplepassword"<br/>} | "Username must not be empty or all white-space." | 400 |
| POST | {<br />  "username": " ",<br/> "password": "examplepassword"<br/>} | "Username must not be empty or all white-space." | 400 |
| POST | {<br />  "username": "2short",<br/> "password": "examplepassword"<br/>} | "Username must be between 8 and 20 characters long." | 400 |
| POST | {<br />  "username": "exampleusername",<br/> "password": ""<br/>} | "Password must not be empty or all white-space." | 400 |
| POST | {<br />  "username": "exampleusername",<br/> "password": " "<br/>} | "Password must not be empty or all white-space." | 400 |
| POST | {<br />  "username": "exampleusername",<br/> "password": "2short"<br/>} | "Password must be at least 8 characters long." | 400 |

## Logging in and out - POST and DELETE on '/auth/sessions'
| Method | Request Body | Response Body | Status Code |
| --- | --- | --- | --- |
| POST | {<br />  "username": "validusername",<br/> "password": "validpassword"<br/>} | {<br/>"logged_in": true,<br/>"user": {<br/>"id": unique integer id,<br/>"username": "exampleusername"<br/>}<br/>} | 200 |
| POST | {<br />  "username": "validusername",<br/> "password": "invalidpassword"<br/>} | "Invalid login credentials." | 400 |
| POST | {<br />  "username": "invalidusername",<br/> "password": "password"<br/>} | "Invalid login credentials." | 400 |
| DELETE | NONE (cookie-header-based) | {<br/>"logged_in": false<br/>} | 200 |

## Checking for whether a user is logged in - GET on '/auth/logged_in'
| Method | Request Body | Response Body | Status Code |
| --- | --- | --- | --- |
| GET | NONE (cookie-header-based) | {<br/>"logged_in": true,<br/>"user": {<br/>"id": unique integer id,<br/>"username": "exampleusername"<br/>}<br/>}  | 200 |
| GET | NONE (cookie-header-based) | {<br/>"logged_in": false<br/>} | 200 |

This project was partially completed in fulfillment of the requirements of COMP 426 with Dr. Ketan Mayer-Patel at the University of North Carolina at Chapel Hill in spring 2021.
