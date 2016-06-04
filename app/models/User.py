""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class User(Model):
    def __init__(self):
        super(User, self).__init__()
    
    def create_user(self, info):

        errors = []

        if len(info['name']) < 3:
            errors.append('name must be at least 3 characters long')
        elif len(info['username']) < 3:
            errors.append(' username must be at least 3 characters long')
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['conpass']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['password']
            pw_hash = self.bcrypt.generate_password_hash(password)
            create_query = "INSERT INTO users (username, name, pw_hash, created_at) VALUES (:username, :name, :pw_hash, NOW())"
            create_data = { 'username': info['username'],
                           'name': info['name'], 
                           'pw_hash': pw_hash,
                          }
            self.db.query_db(create_query, create_data)
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }
    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE username = :username LIMIT 1"
        user_data = {'username': info['username']}
        user = self.db.query_db(user_query, user_data)
        if user:
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return { "status": True, "user": user[0] }
        return {"status": False}
    
    def get_user(self, user_id):
        user_query = "SELECT * FROM users WHERE id = :user_id"
        user_data = {'user_id': user_id }
        return self.db.query_db(user_query, user_data)