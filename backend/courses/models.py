from django.db import models
from accounts.models import Department, Level , User 

class Tag(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name 

class Course(models.Model):
    title = models.CharField()
    description = models.TextField(blank=True,null=True)
    instructor = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    allowed_depts = models.ManyToManyField(Department,blank=True,null=True)
    allowed_levels = models.ManyToManyField(Level,blank=True,null=True)

    def __str__(self):
        return self.title 
    
class Topic(models.Model):
    name = models.CharField()
    resource_link = models.URLField(null=True,blank=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='topics')

    def __str__(self):
        return self.name 


class Enrollment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="enrollments")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="enrollments")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " Enrolled in " + self.course.title 


