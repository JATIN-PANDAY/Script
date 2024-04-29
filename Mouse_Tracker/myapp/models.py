from django.db import models
from base.models import BaseModel

# Create your models here.

class User(BaseModel):
    
    email=models.CharField(max_length=100,blank=True,null=True)
    password=models.CharField(max_length=100,blank=True,null=True)
