from django.db import models
from courses.models import Course 
from accounts.models import User 

class Assignment(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="assignments")
    title = models.CharField()
    description = models.TextField()
    deadline = models.DateTimeField()

    def __str__(self):
        return self.title + " " + self.course.title 
    

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment,on_delete=models.CASCADE,related_name="submissions")
    submitted_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="submissions")
    file = models.FileField(upload_to="submissions/")
    submitted_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True,blank=True)

    class Meta:
        unique_together = ['assignment','submitted_by']

    def __str__(self):
        return self.submitted_by.username + " " + str(self.assignment)
    

class SubmissionGrade(models.Model):
    submission = models.OneToOneField(Submission,on_delete=models.CASCADE,related_name="grade")
    review_text = models.TextField()
    grade = models.DecimalField(max_digits=3,decimal_places=1)
    graded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.grade + " for " + str(self.submission)
    
    