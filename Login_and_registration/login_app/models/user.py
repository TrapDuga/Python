from login_app.config.MySQLconnection import connect
from login_app import bcrypt,DATABASE
from flask import flash
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]+$')
# add bcrypt

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    



    @classmethod
    def register(cls,form):
        password_hash = bcrypt.generate_password_hash(form['password'])
    
        form_data = {
        **form,
        'password' : password_hash
        }
        query = "INSERT INTO tbl_users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s)"
        results = connect(DATABASE).run_query(query,form_data)
        return results


    @classmethod
    def get_by_id(cls,id):
        query = "SELECT * FROM tbl_users WHERE id = %(id)s"
        results = connect(DATABASE).run_query(query, {"id":id})
        return cls(results[0])

    @classmethod
    def get_email(cls,email):
        data = {
            "email" : email
        }
        query = "SELECT * FROM tbl_users WHERE email = %(email)s"
        results = connect(DATABASE).run_query(query,data)
        if results:
            users = cls(results[0])
            return users
        else:
            return False
        
    @staticmethod
    def validate_register(register):
        is_valid = True
        if len(register['first_name']) < 2:
            flash("First Name is not enough")
            is_valid = False
        if len(register['last_name']) < 2:
            flash("Last Name is lacking")
            is_valid = False
        if not email_regex.match(register['email']):
            flash("Email is not valid")
            is_valid = False
        if User.get_email(register['email']):
            is_valid = False
            flash("Email already in use")
        if register['password'] != register['confirmpassword']:
            flash("Passwords don't match")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(form):
        
        found_user = User.get_email(form['email'])
        if found_user:
            if bcrypt.check_password_hash(found_user.password , form['password']):
                return found_user
            
        else:
            flash('Invalid Login')
            return False
        

