import models
import forms
import collections
from flask_restful import Resource
from flask import jsonify, request

class User(Resource):
    def __init__(self):
        self.args = request.args

    def get(self):
        rows = models.Users.select().where(models.Users.username == self.args['username'])
        if rows.count() == 0:
            return abort_if_user_doesnt_exist(self.args['username'])
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['id'] = row.id
            d['username'] = row.username
            d['email'] = row.email
            objects_list.append(d)
        response = jsonify({'user': objects_list})
        response.mimetype='application/json'
        response.status_code=200
        return response
    
    def post(self):
        #Validation needed here
        try:
            models.Users.create_user(
                username=self.args['username'],
                title = self.args['title'],
                first_name = self.args['first_name'],
                middle_name = self.args['middle_name'],
                last_name = self.args['last_name'],
                phone_number = self.args['phone_number'],
                email = self.args['email'],
                password = self.args['password']
                                    )
            rows = models.Users.select().where(models.Users.username == self.args['username'])
            objects_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['id'] = row.id
                d['username'] = row.username
                d['email'] = row.email
                objects_list.append(d)
            response = jsonify({'user created successfully': objects_list})
            response.mimetype='application/json'
            response.status_code=200
        except:
            response = jsonify({'user was not created': 'incorrect parameters'})
            response.mimetype='application/json'
            response.status_code=400
        return response
    
    def delete(self):
        rows = models.Users.select().where(models.Users.username == self.args['username'])
        if rows.count() == 0:
            return abort_if_user_doesnt_exist(self.args['username'])
        objects_list = []
        for row in rows:
            d = collections.OrderedDict()
            d['username'] = row.username
            objects_list.append(d)
        rows = models.Users.delete().where(models.Users.username == self.args['username'])
        rows.execute()
        response = jsonify({'user deleted successfully': objects_list})
        response.mimetype='application/json'
        response.status_code=200
        return response
    
    def put(self):
        rows = models.Users.select().where(models.Users.username == self.args['username'])
        if rows.count() == 0:
            return abort_if_user_doesnt_exist(self.args['username'])
        q = models.Users.update(email=self.args['email']).where(models.Users.username == self.args['username'])
        q.execute() 
        response = jsonify({'user updated successfully': self.args['username']})
        response.mimetype='application/json'
        response.status_code=200
        return response
    
def abort_if_user_doesnt_exist(username):
    response = jsonify({'user does not exist': username})
    response.mimetype='application/json'
    response.status_code=400
    return response


class Data(Resource):
    def __init__(self):
        self.args = request.args

    def get(self):
        rows = models.DataEntry.select()
        if rows.count() == 0:
            return 'No records found.'

        response = jsonify({'Record count': rows.count()})
        response.mimetype = 'application/json'
        response.status_code = 200
        return response

    def post(self):
        # Validation needed here
        try:
            models.DataEntry.create_entry(
                input1=self.args['input']
            )
            response = jsonify({'Value inserted': self.args['input']})
            response.mimetype = 'application/json'
            response.status_code = 200
        except:
            response = jsonify({'Insert failed': 'incorrect parameter'})
            response.mimetype = 'application/json'
            response.status_code = 400
        return response