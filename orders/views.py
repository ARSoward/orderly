from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from .forms import OrderForm, OrderItemSet
from .models import Order, OrderItem, Product, Business, Connection





def index(request):
    return redirect('/orders/')

@login_required
def orderList(request):
  business_id = request.user.account.business.id
  order_list = list(Order.objects.filter(connection__vendor_id=business_id))
  #for each order, make a formset of order items
  #OrderItemList = forms.modelformset_factory(OrderItem, fields=['quantity', 'filled'], extra=0, queryset=OrderItems.filter(Order=))
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
  context = {'business': business}
  try:
    connection = Connection.objects.get(vendor=request.user.account.business.id, customer=business)
    context['connection'] = connection
  except:
    pass
  if request.method == 'POST':
    formset = OrderItemSet(request.POST)
    form = OrderForm(request.POST)
    if(form.is_valid() and formset.is_valid()):
      connection, created = Connection.objects.get_or_create(vendor = business, customer=request.user.account.business)
      order = form.save(commit=False)
      order.connection = connection
      order.save()
      formset = OrderItemSet(request.POST, instance=order)
      formset.is_valid()
      formset.save()
      context['thanks'] = 'Thank you!'
      return render(request, 'orders/about.html', context)
  else:
    formset = OrderItemSet()
    form = OrderForm()
  context.update({'form':form, 'formset': formset})
  #formset(queryset=Product.objects.filter(vendor=business))
  return render(request, 'orders/about.html', context)



@login_required  
def createOrder(request, business_id):
  business = get_object_or_404(Business, id=business_id)
  return render(request, 'orders/list.html', {'business': business, 'error_message': "I'm a work in progress."})
  
