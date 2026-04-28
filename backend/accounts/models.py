""" models related to user accounts"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    DEPT_CHOICES = [
        ("PYTHON","python"),
        ("QA","Qaulity Assurance"),
        ("HR","Human Resources"),
        ("SAES","Sales"),
        ("L&D","Learning and Development"),
    ]
    name = models.CharField(choices=DEPT_CHOICES)

    def __str__(self):
        return self.name 
    
class Level(models.Model):
    LEVEL_CHOICES = [
        ("TRAINEE","trainee"),
        ("JR.","Junior"),
        ("SR.","Senior"),
        ("TEAM-LEAD","Team Lead"),
        ("MANAGER","Manager")]
    level = models.CharField(choices=LEVEL_CHOICES)

    def __str__(self):
        return self.level
    

class EmployeeProfile(models.Model):
    department = models.ForeignKey(Department,null=True,blank=True,on_delete=models.SET_NULL,related_name="employee_profiles")
    manager = models.ForeignKey("self",null=True,blank=True,on_delete=models.SET_NULL,related_name="subordinates")
    level = models.ForeignKey(Level,null=True,blank=True,on_delete=models.SET_NULL,related_name="profiles")

    def __str__(self):
        return str(self.id) 
    
class User(AbstractUser):
    """ User Model """
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    email = models.EmailField(blank=False)
    ROLES = [("LEARNER","learner"),("INSTRUCTOR","instructor")]
    role = models.CharField(choices=ROLES)
    employee_profile = models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE,related_name="accounts")
    def __str__(self):
        """ string representation of User model"""
        return self.username

