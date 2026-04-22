""" models related to user accounts"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    DEPT_CHOICES = [
        ("PY","python"),
        ("QA","Qaulity Assurance"),
        ("HR","Human Resources"),
        ("SL","Sales"),
        ("LD","Learning and Development"),
    ]
    name = models.CharField(choices=DEPT_CHOICES)

    def __str__(self):
        return self.name 
    
class Level(models.Model):
    LEVEL_CHOICES = [
        ("TR","trainee"),
        ("JR","Junior"),
        ("SR","Senior"),
        ("TL","Team Lead"),
        ("MN","Manager")]
    level = models.CharField(choices=LEVEL_CHOICES)
    def __str__(self):
        return self.level 
    

class EmployeeProfile(models.Model):
    department = models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL,related_name="employee_profiles")
    manager = models.ForeignKey("self",null=True,blank=True,on_delete=models.SET_NULL,related_name="subordinates")
    level = models.ForeignKey(Level,null=True,blank=True,on_delete=models.SET_NULL,related_name="profiles")
    user = models.OneToOneField("User",null=True,blank=True,on_delete=models.SET_NULL,related_name="profile")
    def __str__(self):
        return str(self.department) + str(self.level) 
    
class User(AbstractUser):
    """ User Model """
    ROLES = [("LEARN","learner"),("INST","instructor")]
    role = models.CharField(choices=ROLES)
    def __str__(self):
        """ string representation of User model"""
        return self.username
