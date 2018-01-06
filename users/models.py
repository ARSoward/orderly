from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

from django.utils.text import slugify

class Picture(models.Model):
  image = models.ImageField(upload_to = 'user-uploads/')
  caption = models.TextField(null=True, default=None)
  uploaded = models.DateTimeField('uploaded on', default=datetime.now)
  def __str__(self):
    return '%s' % (self.caption)

class Account(models.Model):
  isPremium = models.BooleanField(default=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
  slug = models.SlugField(unique=True, default=slugify(user)) #FIX
  def __str__(self):
    return '%s' % (self.user.first_name)

