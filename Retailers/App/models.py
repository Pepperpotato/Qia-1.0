from django.db import models


# Create your models here.
class Test(models.Model):
    user = models.CharField(max_length=50)
    password = models.CharField(max_length=128)
