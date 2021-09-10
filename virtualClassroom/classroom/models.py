from django.db import models
from django.contrib.auth.models import User
from authService.models import profile
# Create your models here.


class Assignments(models.Model):
    id = models.AutoField(primary_key = True)
    description = models.CharField(max_length=200)
    title = models.CharField(max_length=50)
    assigned_by = models.ForeignKey(profile, related_name="profile_by", on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(profile, related_name="profile_to")
    published_at = models.DateTimeField()
    deadline = models.DateTimeField()
    status = models.CharField(max_length=15)



class Submission(models.Model):
    id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignments,related_name="assignment",on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(profile,related_name="submittedby",on_delete=models.CASCADE)
    time = models.DateTimeField()
    comment = models.CharField(max_length=15)
    status = models.CharField(max_length=25,default="PENDING")

    class Meta:
        unique_together = ('submitted_by','assignment',)
    