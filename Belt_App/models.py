from django.db import models
import re
from time import localtime, strftime, strptime
from datetime import datetime
import bcrypt

class UserManager(models.Manager):
    def create_validator(self, postData):
        errors = {}
        email = User.objects.filter(email=postData['email'])

        if len(postData['first_name']) <2:
            errors['first_name'] = "Name must be more than two characters."
        if len(postData['last_name']) <2:
            errors['last_name'] = "Last name must be more than two characters."
        if len(postData['email']) <2:
            errors['email'] = "Must be a valid email address."
        if len(postData['password']) <8:
            errors['password'] = "Password must be more than 8 characters."
        
        if (postData['password']) != (postData['password_confirm']):
            errors['password'] = "Passwords need to match."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email, try again."

        if len(email) ==1:
            errors ['email'] = "Email is already registered"
        return errors


    def authenticate(self, postData):
        errors = {}
        if len(postData['email']) <2:
            errors['email'] = "Must be a valid email address."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email dude, try again."

        if len(postData['password']) <8:
            errors['password'] = "Password must be more than 8 characters."

        check = User.objects.filter(email=postData['email'])
        if not check:
            errors['email'] = "Email has not been registered."
        else:
            if not bcrypt.checkpw(postData['password'].encode(), check[0].password.encode()):
                errors['email'] = "Email and password do not match."
        return errors


class TripManager(models.Manager):
    def trip_manager(self, postData):
        errors = {}

        if len(postData['destination']) <= 5:
            errors['destination'] = "A destination is required, please fill this in."
        if len(postData['start_date']) <=0:
            errors['start_date'] = "Trip needs a start date."
        if len(postData['end_date']) <=0:
            errors['end_date'] = "Trip needs an end date."
        if len(postData['trip_notes']) <=0:
            errors['trip_notes'] = "This field needs some notes, where ya going?"

        if postData['start_date'] != '' and postData['end_date'] != '':
            
            if datetime.strptime(postData['start_date'], "%Y-%m-%d") < datetime.now():
                errors['start_date'] = "Start date should be in the future."
            # couldn't get this to work. when I hit 'Add trip" it goes to an error page.
            if datetime.strptime(postData['start_date'], "%Y-%m-%d") > datetime.strptime(postData['end_date'], "%Y-%m-%d") :
                errors['trip_start'] = "start needs to be before end date."
        return errors
        # i always forget that return errors thingy



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    trip_notes = models.TextField(max_length=1000)
    creator = models.ForeignKey(User, related_name="trips_uploaded", on_delete = models.CASCADE)
    users_added = models.ManyToManyField(User, related_name="added_trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()