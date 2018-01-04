from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from orders.models import Business
from .models import Account



class UserForm(UserCreationForm):
  email = forms.EmailField(max_length=254)
  account = forms.ModelChoiceField(queryset = Business.objects.all()) #FIX
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'account',)
  #users can only sign up with a registration code, linking them to an existing business.
  
class ContactForm(forms.Form):
  your_name = forms.CharField(max_length=254)
  business_name = forms.CharField(max_length=254)
  email = forms.EmailField(max_length=254)
  website = forms.CharField(max_length=254)
  
