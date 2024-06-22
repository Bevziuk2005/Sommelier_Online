from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    password2 = models.CharField(max_length=128,default='')

class Bottle(models.Model):
    KIND_CHOICES = [
        ('червоне', 'Червоне'),
        ('біле', 'Біле'),
        ('рожеве', 'Рожеве'),
        ('десертне', 'Десертне'),
        ('ігристе', 'Ігристе'),
    ]

    name_ua = models.CharField(max_length=200, default="")  # name
    name_eng = models.CharField(max_length=200, default="")
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='')  #   red/white/rose
    dominant_notes = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=100, default='')  # country
    taste = models.CharField(max_length=500, default='')    # without eat

class Favourites(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    bottle = models.ForeignKey(Bottle, on_delete=models.CASCADE)

class Feedback(models.Model):
    name = models.CharField(max_length=500, default='anonim')
    time = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField()

