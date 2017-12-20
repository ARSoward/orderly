from django.db import models
from django.contrib.auth.models import User
from datetime import date
from orders import models as orderModels #link to objects from another app in same folder

from django.utils.text import slugify

class Account(models.Model):
    isPremium = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    business = models.OneToOneField(orderModels.Business, related_name='account', null=True, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True)
    def __str__(self):
      return '%s, %s' % (self.user.first_name, self.business.business_name)

