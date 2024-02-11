from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe 
from django.utils.html import format_html 
from django.template.defaultfilters import truncatechars
# Create your models here.


class StudentUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=255,null=True)

    def __str__(self) -> str:
        return self.user.username



class Recruiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=255,null=True)
    company=models.CharField(max_length=255,null=True)
    type=models.CharField(max_length=255,null=True)
    status=models.CharField(max_length=255,null=True)

    def __str__(self) -> str:
        return self.user.username





class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date=models.DateField()
    title=models.FileField(null=True)
    salary=models.FloatField(max_length=40)
    image=models.FileField()
    description=models.CharField(max_length=255)
    experience=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    skills=models.CharField(max_length=255)
    creation_date=models.DateField()

    def __str__(self) -> str:
        return self.title


class Apply(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser,on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    apply_date=models.DateField()

    def __str__(self) -> str:
        return self.id
    

    