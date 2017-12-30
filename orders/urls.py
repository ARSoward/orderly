from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from . import views


app_name='orders'
urlpatterns = [        
    # ex: /orders/business_id
    path('orders/', views.orderList, name='orders'),
    
    # ex: /business_id/products
    path('<slug:slug>/products/', views.productList, name='products'),
    
    # ex: /old-windmill-dairy/
    path('<slug:slug>/', views.about, name='about'),

    
    # index page will redirect people depending on their status
    path('', views.index, name='index'),
]

