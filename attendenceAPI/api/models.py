from django.db import models
import os
import datetime

# Create your models here.
class Attendee(models.Model):
    def path_and_rename(instance, filename):
        upload_to = 'imges'
        ext = filename.split('.')[-1]
        email_name = instance.email.split('@')[0]
        # get filename
        if instance.name:
            filename = '{}_{}_.{}'.format(instance.name,instance.id, ext)
        else:
            filename = '{}_{}_.{}'.format(email_name,instance.id, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=100,blank=True,null= True)
    email = models.EmailField(max_length=100, unique= True)
    phone = models.CharField(max_length=100, blank=True,null= True)
    password = models.CharField(max_length=300)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to=path_and_rename, default='imges/default.png')
    profile_img = models.ImageField(upload_to='api/static/profile_img/', default='api/static/profile_img/default.png')
    address = models.CharField(max_length=100, blank=True,null= True, default="Update address")
    pin = models.IntegerField(blank=True,null= True,default=0)
    class_sec = models.CharField(max_length=10, blank=True,null= True, default="update")
    last_name = models.CharField(max_length=100, blank=True,null= True)

    def __str__(self):
        return self.name


class AttendanceLog(models.Model):

    def current_year():
        today = datetime.date.today()
        return today.year
    def current_month():
        today = datetime.date.today()
        return today.month
    def current_day():
        today = datetime.date.today()
        return today.day

    id = models.AutoField(primary_key=True)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    year = models.IntegerField(default=current_year)
    month = models.IntegerField(default=current_month)
    day = models.IntegerField(default=current_day)

    def __str__(self):
        return self.attendee.email
