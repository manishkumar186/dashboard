from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Register(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    address = models.TextField(max_length=250)
    user_type = models.CharField(max_length=250)
    profile_pic = models.ImageField(upload_to='photos/%Y/%m/%d/')

    def __str__(self):
        return self.user.username