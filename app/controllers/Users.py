from system.core.controller import *

# routes['default_controller'] = 'Users'
# routes['POST']['/users/create'] = 'Users#add'
# routes['GET']['/success'] = 'Users#success'
# routes['POST']['/login'] = 'Users#login'

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        # Note that we have to load the model before using it
        self.load_model('User')

    def index(self):
        return self.load_view('loginregister.html')

    # We would set up a GET route for this method
    def show(self, user_id):
        user = self.models['User'].get_user_by_id(user_id)
        return self.load_view('show.html', user=user)

    # We would set up a POST route for this method
    def add(self):
        user_details = {
            'firstname': request.form['firstname'],
            'lastname': request.form['lastname'],
            'email': request.form['email'],
            'password':request.form['password'],
            'confirmpw':request.form['confirmpw']
        }
        print user_details
        add = self.models['User'].add_user(user_details)
        print add
        if add['status'] == True:
            session['id'] = add['user']['user_id']
            session['name'] = add['user']['firstname']
            return redirect('/success')
        else:
            for message in add['errors']:
                flash(message, 'reg_error')
            return redirect('/')
    def success(self):
        return self.load_view('success.html')

    def login(self):
        login_details = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        data = self.models['User'].login(login_details)
        if data['status'] == True:
            session['id'] = data['user']['user_id']
            session['name'] = data['user']['firstname']
            return redirect('/success')
        else:
            for message in data['errors']:
                flash(message, 'reg_error')
            return redirect('/')
        return redirect('/')

    # We would set up a POST route for this method
    def update(self, user_id):
        user_details = {
            'id': request.form['user_id'],
            'title': request.form['name'],
            'description': request.form['name']
        }
        self.models['User'].update_user(user_details)
        return redirect('/')

     # This is how a method used to delete a user would look
     # We would set up a POST route for this method
    def delete(self, user_id):
         self.models['User'].delete_user(user_id)
         return redirect('/')
