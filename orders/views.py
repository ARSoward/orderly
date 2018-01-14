from __future__ import unicode_literals
from django.shortcuts import get_object_or_404, get_list_or_404, render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django import forms
from django.forms.models import model_to_dict
from .forms import OrderForm, OrderItemSet, OrderItemModelSet
from .models import Order, OrderItem, Product, Business, Connection
from django.contrib.auth.forms import AuthenticationForm
from users.forms import ContactForm
from django_mailbox.models import Mailbox 

def index(request):
    if not request.user.is_authenticated:
      context = {'loginform': AuthenticationForm(), 'contactform': ContactForm()}
      return render(request, 'orders/index.html', context)
    else:
      return HttpResponseRedirect(reverse('orders:orders'))
  
@login_required
def orderList(request, status='C'):
  businessID = request.user.account.business.id
  rawList = list(Order.objects.filter(connection__vendor_id=businessID, status=status).order_by('requested_delivery'))
  #OrderItemList = forms.modelformset_factory(OrderItem, fields=['quantity', 'filled'], extra=0, queryset=OrderItems.filter(Order=))
  business = get_object_or_404(Business, id=businessID)
  orderList = []
  number = 0
  if status == 'O': #TODO outgoing orders
    pass 
  ##TODO:
  # changes to orderform are not saved (notes, date)
  # form and formset are saved regardless if they are invalid
  # pending order submits automatically on change (will need to make it a parameter for formset creation)
  if(request.user.account.isPremium):
    mailbox = Mailbox.objects.get(name = businessID)
    mailbox.get_new_mail()
    print("mail checked")
  if status == 'P':
    for order in rawList:
      form = OrderForm(instance=order, prefix=str(number))
      if OrderItem.objects.filter(order = order):
        formset = OrderItemModelSet(request.POST or None, prefix=str(number), queryset=OrderItem.objects.filter(order = order))
        emailOrder = False
      else:
        formset = OrderItemSet(request.POST or None, prefix=str(number))
        emailOrder = True
      number += 1
      if (request.method == 'POST'):
        if emailOrder:
          formset = OrderItemSet(request.POST, instance=order)
          formset.is_valid()
          formset.save()
        else:
          instances = formset.save()
        form.is_valid()
        order = form.save(commit=False)
        order.status = 'C'
        order.save()
        return HttpResponseRedirect(reverse('orders:pending'))
      orderList.append({'business': order.connection.customer,
                        'orderForm': form,
                        'orderItemFormset': formset,
                        'order': order,
                        'status': order.status,
                      })
    template = 'orders/pendingorderlist.html'
  else:
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
    if status == 'C':
      template = 'orders/orderlist.html'
    else:
      template = 'orders/historyorderlist.html'
  context = {'list': orderList, 'business': business}
  return render(request, template, context)
  
@login_required
def productList(request, slug):
  business = get_object_or_404(Business, account__slug=slug)
  products = business.products.all;
  context = {'business': business, 'list': products}
  return render(request, 'orders/products.html', context)
 
def about(request, slug): 
  business = get_object_or_404(Business, account__slug=slug)
  products = business.products.all;
  context = {'business': business, 'products':products, 'slug': slug}
  contactFields = ['contact_name','website','email','email','address']
  contacts = model_to_dict(business, contactFields)
  try:
    connection = Connection.objects.get(vendor=request.user.account.business.id, customer=business)
    contacts.append({'notes': connection.notes})
  except:
    pass
  context.update({'contacts': contacts});
  form = OrderForm(request.POST or None)
  formset = OrderItemSet(request.POST or None)
  for f in formset:
    f.fields['product'].queryset=(Product.objects.filter(vendor=business))
  context.update({'form':form, 'formset': formset})
  #TODO form processing - will eventually move to it's own view.
  if request.method == 'POST':
    if(form.is_valid() and formset.is_valid()):
      connection, created = Connection.objects.get_or_create(vendor = business, customer=request.user.account.business)
      order = form.save(commit=False)
      order.connection = connection
      order.save()
      formset = OrderItemSet(request.POST, instance=order)
      formset.is_valid()
      formset.save()
      context.update({'thanks':'Thank you!'})
      return render(request, 'orders/about.html', context)
  #formset(queryset=Product.objects.filter(vendor=business))
  return render(request, 'orders/about.html', context)

@login_required  
@login_required
def newOrder(request):
  formset = OrderItemSet(request.POST or None)
  form = OrderForm(request.POST or None)
  if(form.is_valid() and formset.is_valid()):
    connection, created = Connection.objects.get_or_create(vendor = business, customer=request.user.account.business)
    order = form.save(commit=False)
    order.connection = connection
    order.save()
    formset = OrderItemSet(request.POST, instance=order)
    formset.is_valid()
    formset.save()
    context['thanks'] = 'Thank you!'
  next = request.POST.get('next', '/')
  return HttpResponseRedirect(request, next)
  
