from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from orders import models as orderModels #link to objects from another app in same folder

from django.utils.text import slugify
      
class Picture(models.Model):
  image = models.ImageField(upload_to = 'user-uploads/')
  caption = models.TextField(null=True, default=None)
  uploaded = models.DateTimeField('uploaded on', default=datetime.now)
  
class Account(models.Model):
  business = models.OneToOneField(orderModels.Business, related_name='account', null=True, on_delete=models.CASCADE)
  def makeSlug(instance):
    slug = orig = slugify(instance.business)[:50]
    for x in itertools.count(1):
      if not Account.objects.filter(slug=instance.slug).exists():
        break
      instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
    return slug
  isPremium = models.BooleanField(default=False)
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
  about = models.TextField(max_length=600, null=True, default=None)
  slug = models.SlugField(unique=True, default=makeSlug)
  address = models.TextField(null=True, default=None)
  website = models.TextField(null=True, default=None)
  phone = models.TextField(null=True, default=None)
  picture = models.OneToOneField(Picture, related_name='owner', null=True, on_delete=models.CASCADE)
  def __str__(self):
    return '%s, %s' % (self.user.first_name, self.business.business_name)

