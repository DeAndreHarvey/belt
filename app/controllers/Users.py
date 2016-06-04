"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
       
        self.load_model('User')
        self.load_model('Trip')
        self.db = self._app.db

        
   
    def index(self):
       return redirect('/main')

    def main(self):
        return self.load_view('index.html')
    def register(self):
        user_info = {
            "name" : request.form['name'],
            "username" : request.form['username'],
            "password" : request.form['password'],
            "conpass" : request.form['conpass'],
        }
        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['name'] = create_status['user']['name']
            
            return redirect('/travels')
        else:
            
            for message in create_status['errors']:
                flash(message)
            return redirect('/main')

    def login(self):
        user_info ={
        "username" : request.form['username'],
        "password" : request.form['password']
            }
        login_status = self.models['User'].login_user(user_info)
        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['name'] = login_status['user']['name']
            
            return redirect('/travels')
        else:
            flash("invalid login")
            return redirect('/main')
    def travels(self):
        travels = self.models['Trip'].get_trips()
        added = self.models['Trip'].get_addedtrips(session['id'])
        usertrips = self.models['Trip'].get_trip_by_id(session['id'])
        joined= self.models['Trip'].get_usertrips_by_id(session['id'])
        print travels
        return self.load_view('travels.html', trips = travels, usertrips=usertrips, joined=joined, added =added)
    
    def travels_add(self):
        return self.load_view('add.html')
        
    
    def add_trip(self, user_id):
        dest =request.form['dest']
        description =request.form['description']
        dfrom = request.form['from']
        dto = request.form['to']
        add_status = self.models['Trip'].add_trip(dest, description, user_id, dfrom, dto)
        if add_status['status'] == True:
           
            return redirect('/travels')
        else:
            
            for message in add_status['errors']:
                flash(message)
            return redirect('/travels/add')
        
        
    def show(self, trips_id):
        trip =self.models['Trip'].get_trip_by_tripsid(trips_id)
        return self.load_view('show.html', trip=trip[0])
    
    def logout(self):
        session.clear
        return redirect('/main')
    def add_userstrips(self,  trips_id):
        user_id = session['id']
        self.models['Trip'].add_userstrips(trips_id, user_id)
        return redirect('/travels')
    
    def delete_fav(self, fav_id):
        self.models['Quote'].delete_fav(fav_id)
        return redirect('/quotes')
        
        
        
    