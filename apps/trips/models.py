from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import date, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PSWD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$')

class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        if len (postData['first_name']) < 2:
            errors ['first_name_error'] = "At least 2 characters needed."
        if len (postData['last_name']) < 2:
            errors ['last_name_error'] = 'At least 2 characters needed.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_error'] = "Email already exists."
        if not PSWD_REGEX.match(postData['password']):
            errors["password_error"] = 'Not a valid password'
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password_error'] = 'Confirmation password does not match'
        return errors

    def register(self, postData):
        hashed_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        userid = self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_pw
        ).id
        return userid

    def login(self, postData):
        errors={}
        user = self.filter(email = postData['email'])
        print(user.values())
        if len(user) == 0:
            errors['login_user_error'] = "Email you entered does not exist"
            return errors
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['login_pswd_error'] = "Password does not match"
            return errors
        else:
            user_id = user[0].id
            hashed_id = bcrypt.hashpw(str(user_id).encode(), bcrypt.gensalt())
            return
        return errors 

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.TextField()
    objects = UserManager()

class TripManager(models.Manager):
    def trip_validator(self, postData):
        errors = {}
        if len(postData["destination"]) < 3:
            errors["destination"] = "Destination must be at least 3 characters."
        if len(postData["startdate"]) > 0 and datetime.strptime(postData["startdate"], '%Y-%m-%d') < datetime.today() :
            errors["startdate"] = "Invalid start date."
        if len(postData["enddate"]) > 0 and datetime.strptime(postData["enddate"], '%Y-%m-%d') < datetime.now() :
            errors["enddate"] = "Invalid end date."
        if len(postData["plan"]) < 3 and len(postData['plan']) != 0:
            errors["plan"] = "Plan must have 3 characters or left blank."
        return errors


class trips(models.Model):
    destination = models.CharField(max_length=255)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    plan = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
