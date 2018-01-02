from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from orders import models as orderModels #link to objects from another app in same folder

from django.utils.text import slugify
      
class Picture(models.Model):
  image = models.ImageField()
  caption = models.TextField(null=True, default=None)
  uploaded = models.DateTimeField('uploaded on', default=datetime.now)
  
class Account(models.Model):
    isPremium = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    about = models.TextField(max_length=600, null=True, default=None)
    slug = models.SlugField(unique=True, default=slugify(user))
    address = models.TextField(null=True, default=None)
    website = models.TextField(null=True, default=None)
    phone = models.TextField(null=True, default=None)
    business = models.OneToOneField(orderModels.Business, related_name='account', null=True, on_delete=models.CASCADE)
    picture = models.OneToOneField(Picture, related_name='owner', null=True, on_delete=models.CASCADE)
    def __str__(self):
      return '%s, %s' % (self.user.first_name, self.business.business_name)
