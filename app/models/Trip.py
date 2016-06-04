""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
from datetime import datetime

class Trip(Model):
    def __init__(self):
        super(Trip, self).__init__()
   
    def get_trips(self):
        query = "select * from trips left join users on trips.user_id= users.id"
        return self.db.query_db(query)
    
    def get_addedtrips(self,user_id):
        query = "select a.* from(select users_trips.id, users_trips.user_id,users_trips.trip_id,trips.dest,trips.description,trips.user_id as tuser_id,users2.name,trips.dfrom, trips.dto  from users_trips left join users on users_trips.user_id= users.id left join trips on  users_trips.trip_id = trips.id left join users as users2 on trips.user_id = users2.id where users_trips.user_id = :user_id)a"
        data ={
                'user_id' : user_id
                }
        return self.db.query_db(query,data)
    
    def add_trip(self, dest, description, user_id, dfrom, dto):
        errors = []

        if not dest:
            errors.append('destination cannot be blank')
        if not description:
            errors.append('description cannot be blank')
        if not dfrom:
            errors.append('Date From cannot be blank')
        if not dto:
            errors.append('Date to cannot be blank')
        if dfrom > dto:
            errors.append('Date to must be after Date From')
#        if dfrom < datetime.today().date():
#            errors.append('Date must be future date')
        if errors:
            return {"status": False, "errors": errors}
        else:
            sql = "INSERT INTO trips (dest, description, user_id, dfrom, dto) Values(:dest, :description, :user_id, :dfrom,  :dto)"
            data ={
                'dest':dest,
                'description':description,
                'user_id': user_id,
                'dfrom': dfrom,
                'dto': dto
                }
            self.db.query_db(sql, data)
            return { "status": True }
    
    def get_trip_by_id(self, user_id):
        query = "select * from trips left join users on trips.user_id= users.id where user_id = :user_id"
        data ={
            'user_id': user_id
        }
        return self.db.query_db(query,data)
    
    def get_trip_by_tripsid(self, trips_id):
        query = "select * from trips left join users on trips.user_id= users.id  where trips.id = :trips_id"
        data ={
            'trips_id': trips_id
        }
        return self.db.query_db(query,data)
    
    def add_userstrips(self, trips_id, user_id):
        sql = "INSERT INTO users_trips (trip_id, user_id) Values(:trips_id, :user_id)"
        data ={
            'trips_id':trips_id,
            'user_id': user_id
            }
        self.db.query_db(sql, data)
        return True
    def get_usertrips_by_id(self, user_id):
        query = "select users_trips.id, users_trips.user_id,users_trips.trip_id,trips.dest,trips.description,trips.user_id as tuser_id,users2.name,trips.dfrom, trips.dto  from users_trips left join users on users_trips.user_id= users.id left join trips on  users_trips.trip_id = trips.id left join users as users2 on trips.user_id = users2.id where users_trips.user_id = :user_id"
        data ={
            'user_id': user_id
        }
        return self.db.query_db(query,data)
    
   