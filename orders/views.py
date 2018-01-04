from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, get_list_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from .forms import OrderForm, OrderItemSet, OrderItemModelSet
from .models import Order, OrderItem, Product, Business, Connection
from django.contrib.auth.forms import AuthenticationForm
from users.forms import ContactForm 


def index(request):
    context = {'loginform': AuthenticationForm(), 'contactform': ContactForm()}
    return render(request, 'orders/index.html', context)
    #return redirect('/orders/')
  
@login_required
def orderList(request, status='C'):
  businessID = request.user.account.business.id
  rawList = list(Order.objects.filter(connection__vendor_id=businessID, status=status).order_by('requested_delivery'))
  #OrderItemList = forms.modelformset_factory(OrderItem, fields=['quantity', 'filled'], extra=0, queryset=OrderItems.filter(Order=))
  business = get_object_or_404(Business, id=businessID)
  orderList = []
  number = 0
  for order in rawList:
    formset = OrderItemModelSet(request.POST or None, prefix=str(number), queryset=OrderItem.objects.filter(order = order))
    number += 1
    if (request.method == 'POST'):
      instances = formset.save()
      order.save()
    orderList.append({'business': order.connection.customer,
                      'orderItemFormset': formset,
                      'order': order,
                      'status': order.status,
                    })
  context = {'list': orderList, 'business': business}
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
  formset = OrderItemSet(request.POST or None)
  form = OrderForm(request.POST or None)
  if request.method == 'POST':
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
  context.update({'form':form, 'formset': formset})
  #formset(queryset=Product.objects.filter(vendor=business))
  return render(request, 'orders/about.html', context)

@login_required  
def createOrder(request, business_id):
  business = get_object_or_404(Business, id=business_id)
  return render(request, 'orders/list.html', {'business': business, 'error_message': "I'm a work in progress."})
  
