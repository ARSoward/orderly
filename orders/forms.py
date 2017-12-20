from django import forms
from datetime import date, timedelta
from .models import Business, Order, Product, Connection, OrderItem
from ajax_select.fields import AutoCompleteSelectField, AutoCompleteSelectMultipleField
from ajax_select import make_ajax_field

#create new business, modify business details    
class BusinessForm(forms.Form):
  class Meta:
    model = Business
    fields = all
  business_name = AutoCompleteSelectField("business")
  contact_name = forms.CharField(max_length=60)
  website = forms.URLField(max_length=200, required=False)
  email = forms.EmailField(max_length=254, required=False)
  phone = forms.CharField(max_length=15, required=False)
  address = forms.CharField(max_length=260, required=False)

#create new order, modify my orders
class OrderForm(forms.BaseModelFormSet):
  FREQUENCY_CHOICES = (
    ('S', 'just this once'),
    ('W', 'weekly'),
    ('M', 'monthly'),
    ('B', 'every other month'),
  )
  requested_delivery = forms.DateField(widget=forms.SelectDateWidget, initial=date.today() + timedelta(days=7))
  standing_order_frequency = forms.ChoiceField(choices = FREQUENCY_CHOICES, label='Reoccurs')
  notes = forms.CharField(widget=forms.Textarea, required=False)

#add new product to productList
class ProductForm(forms.Form):
  class Meta:
    model = Product
  name = forms.CharField(max_length=200)
  description = forms.CharField(max_length=600, required=False)
  price = forms.DecimalField(max_digits=5, decimal_places=2, initial=1.00)
  unit = forms.CharField(max_length=11, initial='unit') 
  #image field once pillow is imported
  
class ConnectForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ['vendor']
  vendor = AutoCompleteSelectField("business")
    
