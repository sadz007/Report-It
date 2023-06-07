from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def valid_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email =%(email)s;"
        results = connectToMySQL("python_schema").query_db(query,user)

        if len(results) >= 1:
            flash("Email already exists.","register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email. You need to.", "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False
        if len(user['password']) <8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
        if user['password'] != user['confirmpassword']:
            flash("Password does not match.","register")
        return is_valid


    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        results = connectToMySQL("python_schema").query_db(query,data)
        print(results)
        return results

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("python_schema").query_db(query)
        users =[]
        for x in results:
            users.append(cls(x))
            print("This is the User", users)
        return users

    @classmethod
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("python_schema").query_db(query,data)
        if len(results)< 1 :
            return False
        return cls(results[0]) 

    @classmethod
    def get_id(cls,id):
        data = {
            "id": id
        }
        query = "SELECT * FROM users WHERE id = %(id)s;"
        print(query)
        
        
        results = connectToMySQL("python_schema").query_db(query,data)
        if len(results) < 1 :
            return False
    
        
        print("LINE 85" , query)
        return cls(results[0]) 
