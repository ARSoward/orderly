from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from .forms import OrderForm, BusinessForm, ProductForm, ConnectForm
from .models import Order, OrderItem, Product, Business, Connection
from ajax_select.fields import AutoCompleteSelectField




def index(request):
    return redirect('/orders/')

@login_required
def orderList(request):
  business_id = request.user.account.business.id
  order_list = list(Order.objects.filter(connection__vendor_id=business_id))
  business = get_object_or_404(Business, id=business_id)   
  context = {'list': order_list, 'business': business}
  return render(request, 'orders/orderlist.html', context)
  
@login_required
def productList(request, slug):
  business = get_object_or_404(Business, account__slug=slug)
  list = business.products.all;
  context = {'business': business, 'list': list}
  return render(request, 'orders/products.html', context)
  
def about(request, slug): 
  business = get_object_or_404(Business, account__slug=slug)
  form = OrderForm()
  formset = forms.modelformset_factory(OrderItem, fields=('product','quantity',),
            widgets = { 'product': AutoCompleteSelectField("product", help_text=None)}) 
            #'NoneType' object has no attribute '_default_manager'
  formset(queryset=Product.objects.filter(vendor=business))
  try:
    connection = Connection.objects.get(vendor=request.user.account.business.id, customer=business)
  except ObjectDoesNotExist:
    connection = None
  if connection:
    context = {'business': business, 'connection' : connection, 'form': form, 'formset': formset }
  else:
    context = {'business': business, 'form': form, 'formset': formset }
  return render(request, 'orders/about.html', context) #change to account id when implemented



@login_required  
def createOrder(request, business_id):
  business = get_object_or_404(Business, id=business_id)
  return render(request, 'orders/list.html', {'business': business, 'error_message': "I'm a work in progress."})
  
