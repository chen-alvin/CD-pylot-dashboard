from system.core.model import Model
import re
class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def get_all_users(self):
        return self.db.query_db("SELECT * FROM users")

    def get_user_by_id(self, user_id):
        # pass data to the query like so
        query = "SELECT * FROM users WHERE user_id = :user_id"
        data = {'user_id': user_id}
        return self.db.query_db(query, data)

    def add_user(self, user):
        # Build the query first and then the data that goes in the query
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        if not user['firstname']:
            errors.append('First name cannot be blank')
        elif len(user['firstname']) < 2:
            errors.append('First name must be at least two characters')
        if not user['lastname']:
            errors.append('Last name cannot be blank')
        elif len(user['lastname']) < 2:
            errors.append('Last name must be at least two characters')
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Email format must be valid')
        if not user['password']:
            errors.append('Password cannot be blank')
        elif len(user['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user['password'] != user['confirmpw']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(user['password'])
            query =  "INSERT INTO users (firstname, lastname, email, pw_hash, created_at) \
                      VALUES (:first, :last, :email, :pw_hash, NOW())"
            data = { 'first': user['firstname'], 'last': user['lastname'], 'email': user['email'], 'pw_hash': pw_hash }
            self.db.query_db(query,data)
            get_user = "SELECT * from users where email = :email limit 1"
            data = {'email':user['email']}
            user = self.db.query_db(get_user,data)
            print user
            return {"status": True, "user":user[0]}

    def login(self,login_details):
        errors = []
        print login_details
        user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
        query_data = { 'email': login_details['email'] }
        user = self.db.query_db(user_query, query_data)
        print user
        if user == []:
            errors.append('Invalid email/password combination')
            return {"status":False, "errors":errors}
        else:
            if not self.bcrypt.check_password_hash(user[0]['pw_hash'],login_details['password']):#login fails
                errors.append('Invalid email/password combination')
                return {"status":False, "errors":errors}
        if self.bcrypt.check_password_hash(user[0]['pw_hash'],login_details['password']):#login success
            return {"status": True, "user":user[0]}
        return 'test'

    def update_user(self, user):
        # Building the query for the update
        query = "UPDATE users SET title=:title, description=:description WHERE id = :user_id"
        # we need to pass the necessary data
        data = { 'title': user['title'], 'description': user['description'], 'user_id': user['id']}
        # run the update
        return self.db.query_db(query, data)

    def delete_user(self, user_id):
        query = "DELETE FROM users WHERE user_id = :user_id"
        data = { "user_id": user_id }
        return self.db.query_db(query, data)
