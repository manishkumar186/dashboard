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

class Blog(models.Model):
    status = (
        ("Draft","Draft"),
        ("Published","Published")
    )
    title = models.CharField(max_length=250,unique=True)
    image = models.ImageField(upload_to='blogimage/%Y/%m/%d/')
    category = models.CharField(max_length=250)
    summary = models.CharField(max_length=250)
    content = models.TextField(null=True)
    doctor_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    draft = models.CharField(choices=status,null=True,max_length=50)

    created_on = models.DateTimeField(auto_now_add=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,null=True)


    def __str__(self):
        return self.title

class Appointment(models.Model):
    speciality = models.CharField(max_length=250)
    appointment_date = models.CharField(max_length=250)
    appointment_time = models.CharField(max_length=250)
    patient_name = models.ForeignKey(User,on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=250)
    
    def __str__(self):
        return self.patient_name.first_name+" "+self.patient_name.last_name