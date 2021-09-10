from django.db import models
from django.contrib.auth.models import User
# Create your models here.




#models

class profile(models.Model):
    id = models.AutoField(primary_key = True)
    role = models.CharField(max_length = 15)
    user = models.OneToOneField(User,on_delete = models.CASCADE)

  

