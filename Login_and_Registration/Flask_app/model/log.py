from Flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = "login_reg"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_up = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT into register(first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('register').query_db(query, data)

    @classmethod
    def get(cls):
        query = "SELECT * from register;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
    
    @classmethod
    def get_mail(cls, data):
        query = "SELECT * FROM register WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    @classmethod
    def get_id(cls, data):
        query = "SELECT * FROM register WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


    @staticmethod
    def vaildiate(user):
        is_valid = True
        query = "SELECT * FROM register WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        if len(results) >= 1:
            flash("Email is already taken.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("invaild Email.!", ['register!!'])
        if len(user['first_name']) < 3:
            flash("First name must be 3 letters long!", "register")
            is_valid = False
        if len(user['last_name']) < 3:
            flash("Last name must be 3 letters long!", "register")
            is_valid = False
        if len(user['password']) > 8:
            flash("Password must be 8 Characters long!", "register")
            is_valid = False
        if user['password'] != user['confirm']:
            flash("PASSWORDS DO NOT MATCH", "register")
        return is_valid