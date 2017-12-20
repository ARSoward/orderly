from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import AccountForm
from .models import Account
  
def registerUser(request):
  if request.user.is_authenticated:
    return redirect('/orders/')
  if request.method == 'POST':
    form = AccountForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(request, user)
      account = Account.objects.create(user=username, business = form.cleaned_data.get('account'))
      return redirect('/settings/')
  else:
    form = AccountForm()
    return render(request, 'registration/registration.html', {'form': form})
  #context = {'form': AccountForm()}
  #return render(request, 'registration/registration.html',context)
  
@login_required  
def settings(request):
  account_business = request.user.account.business.business_name
  account_owner = request.user.first_name
  context = {'owner': account_owner, 'business': account_business}
  return render(request, 'registration/settings.html', context)
