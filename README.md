## Description
In this lab you will demonstrate your ability to use message digests for security (authentication) purposes.  You will create a simple application (desktop, mobile, web app, rest api, etc.) that stores user logins in a relational database table.  Then you will allow authentication by comparing provided credentials to the credentials stored in the database.

## Requirements
1. You may use either a SQL or NoSQL datastore, to store login credentials (username and password). Be smart about your data store choice.
2. You must create an application that connects to your datastore.
3. You must allow any anonymous user to register for an account by providing a username and password.
4. You must use, create, and store a salted SHA-256 hash to avoid storing the user's password in plain text in the database.
5. Your salt value must be randomly generated for each user's password and also stored in your database alongside the hash for later retrieval/comparison/login activities
6. You must allow registered users to attempt to login, and then you should compare the credentials they provided on login with the credentials stored in the database.  If they match, the user is authenticated. If they do not match, then refuse access to the application.
7. You must provide your user with the ability to change their password - their username should remain
8. You must enforce some type of basic password complexity rules for your user's chosen passwords. For instance, your passwords might need to require a certain number of letters, numbers, characters, special symbols, non-repeating characters, etc... (While you can certainly write your own algo for this, feel free to leverage a library from your platform of choice.
9. Please demonstrate the complete functionality of your app in any way you see fit. For example, any ONE of these would work just fine (your choice):
  - A simple console app
  - A webapp/webpage/SPA
  - A small mobile app
  - Simple Postman requests demonstrating complete RESTful API calls to a set of endpoints