from django.db import models
from datetime import date, timedelta
from users import models as userModels

class Business(models.Model):
  business_name = models.CharField(max_length=60)
  contact_name = models.CharField(max_length=60)
  website = models.URLField(max_length=200, blank=True)
  email = models.EmailField(max_length=254, blank=True)
  phone = models.CharField(max_length=15, blank=True)
  address = models.CharField(max_length=260, blank=True)
  about = models.TextField(max_length=600, null=True, default=None)
  account = models.OneToOneField(userModels.Account, related_name='business', null=True, default=None, on_delete=models.CASCADE)
  picture = models.OneToOneField(userModels.Picture, related_name='business', blank=True, null=True, on_delete=models.CASCADE)
  #tags, categories, to make businesses searchable
  #various settings: window of time to place orders, 
  def __str__(self):
    return self.business_name
  class Meta:
      verbose_name_plural = "businesses"


class Connection(models.Model):
  vendor = models.ForeignKey(Business, related_name='vendor', on_delete=models.CASCADE)
  customer = models.ForeignKey(Business, related_name='customer', on_delete=models.CASCADE)
  since = models.DateField('connected since', default=date.today)
  notes = models.TextField(max_length=600, blank=True, null=True) #notes that the VENDOR can view/edit.
  def __str__(self):
    return '%s selling to %s' % (self.vendor.business_name, self.customer.business_name)

class Order(models.Model):
  connection = models.ForeignKey(Connection, on_delete=models.CASCADE, default=None) #set to deleted user
  ORDER_STATUS_CHOICES = (
    ('P', 'Pending'),   #user needs to approve order from email or new customer
    ('C', 'Current'),   #current orders show up in the default to-do list
    ('D', 'Delivered'), #delivered orders will be removed from to-do list, but can be searched
  )
  status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES, default='C')
  requested_delivery = models.DateField('requested delivery date', default=(date.today() + timedelta(days=7))) # set to the future to set up recurring orders.
  notes = models.TextField(max_length=600, blank=True)
  def __str__(self):
    return '%s %s' % (self.connection.vendor.business_name, self.requested_delivery.strftime("%B %d, %Y"))
  @property
  def isComplete(self):
    if(date.today() <= self.requested_delivery or any(item.filled == False for item in self.item.all())):
      return False
    return True
  def save(self, *args, **kwargs):
    if self.isComplete:
      self.status = 'D'
    super().save(*args, **kwargs)
  #frequency: will be used to create next order when this one is marked delivered.
  
class Product(models.Model):
  name = models.CharField(max_length=200, unique=True)
  description = models.TextField(max_length=600, blank=True)
  vendor = models.ForeignKey(Business, on_delete=models.CASCADE, default=None, related_name='products')
  price = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
  unit = models.CharField(max_length=11, default='unit') #I want unit and price to be associated in pairs that the user creates.
  picture = models.OneToOneField(userModels.Picture, related_name='product', blank=True, null=True, on_delete=models.CASCADE)
  def __str__(self):
    return self.name
  
class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='item') #many OrderItems have the same Order
  product  = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product') #set to 'deleted item' on delete
  quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
  filled = models.BooleanField(default=False)
  #measure = models.CharField(max_length=11, default='unit')
  def __str__(self):
    return '%s %s' % (self.product.name, self.quantity)
    
    
#notification
  
