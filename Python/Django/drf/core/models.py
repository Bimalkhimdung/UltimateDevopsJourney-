from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=200,blank=False)
    middlename = models.CharField(max_length=200,blank=True)
    lastname = models.CharField(max_length=200,blank=False)
    address = models.CharField(max_length=400,blank=False)
    phonenumber = models.IntegerField(blank=False,unique=True)

class legal_info(models.Model):
    pan_number = models.IntegerField(blank=False)
    citizenship_number = models.IntegerField(blank=False)
