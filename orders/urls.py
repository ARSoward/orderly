from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from . import views


app_name='orders'
namespace='orders'
urlpatterns = [        
  #these three all call orderlist
  path('orders/', views.orderList, name='orders'),
  path('pending/', views.orderList, {'status':'P'} , name='pending'),   
  path('history/', views.orderList,  {'status':'D'}, name='history'),
  
  #processes form and redirects
  path('new-order/', views.newOrder, name='new-order'),
  
  # ex: /owd/products
  path('<slug:slug>/products/', views.productList, name='products'),
  
  # ex: /old-windmill-dairy/
  path('<slug:slug>/', views.about, name='about'),
 
  # index page will redirect people depending on their status
  path('', views.index, name='index'),
]

