'''
User Object-Relational-Mapping (ORM)
'''

import json
import argon2
from backend.db import get_db

class User:
    def __init__(self, id, username, password_hash):
        '''Constructor.'''
        self.id = id
        self.username = username
        self.password_hash = password_hash

    def getUsername(self):
        return self.username

    def getPasswordHash(self):
        return self.password_hash

    def setPasswordHash(self, new_password_hash):
        self.password_hash = new_password_hash
        self.update()

    def update(self):
        '''Writes back instance field values into database.'''
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("UPDATE Users SET username = %s, password_hash = %s WHERE id = %s", (self.username, self.password_hash, self.id))
        db.commit()

    def jsonable(self):
        '''Returns a dict appropriate for creating a JSON representation of the instance.'''
        return {'id': self.id, 'username': self.username}

    @staticmethod
    def userExists(username):
        '''Returns true if there exists a user tuple with the specified username, false otherwise.'''
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        row = cursor.fetchone()
        return True if row is not None else False

    @staticmethod
    def findByUsername(username):
        '''Returns User instance associated with Users tuple uniquely identified by provided username value.
            Otherwise, Exception raised.'''
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if row is None:
            raise Exception(f"No such user with username: {username}")
        else:
            return User(row['id'], row['username'], row['password_hash'])

    @staticmethod
    def verifyValidUser(username, password):
        '''Returns true if user tuple with specified username and password exists, false otherwise.
            If user tuple exists, checks for need to rehash password and updates user's associated
            password_hash in database when appropriate.'''
        try:
            user = User.findByUsername(username)
        except Exception as e:
            return False
        ph = argon2.PasswordHasher()
        password_hash = user.getPasswordHash()
        try:
            ph.verify(password_hash, password)
        except argon2.exceptions.VerifyMismatchError as e:
            return False
        if ph.check_needs_rehash(password_hash):
            user.setPasswordHash(ph.hash(password))
        return True;

    @staticmethod
    def createFromJSON(json_data):
        '''Creates new user instance using dict created from POST '/registrations' request body JSON.
            Raises exceptions as appropriate.'''
        try:
            validateUserData(json_data)
        except Exception as e:
            raise e
        ph = argon2.PasswordHasher()
        password_hash = ph.hash(json_data['password'])
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("INSERT INTO Users (username, password_hash) VALUES (%s, %s)", (json_data['username'], password_hash))
        db.commit()
        return User.findByUsername(json_data['username'])


def validateUserData(json_data):
    '''Given the dict created from the JSON of a POST '/registrations' request body, helps
        ensure that the data provided for the user at hand is appropriate according to
        database specifications by raising exceptions appropriately.'''
    if User.userExists(json_data['username']):
        raise UserDataException(f"Username {json_data['username']} taken.")
    elif not json_data['username'] or json_data['username'].isspace():
        raise UserDataException("Username must not be empty or all white-space.")
    elif not json_data['password'] or json_data['password'].isspace():
        raise UserDataException("Password must not be empty or all white-space.")
    elif len(json_data['username']) < 8 or len(json_data['username']) > 20:
        raise UserDataException("Username must be between 8 and 20 characters long.")
    elif len(json_data['password']) < 8:
        raise UserDataException("Password must be at least 8 characters long.")


class UserDataException(Exception):
    '''Exception raised upon provision of inadequate/erroneous user data.'''
    pass
