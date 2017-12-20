# in project urlconfig, include: url('^', include('django.contrib.auth.urls'))
# create myproject/shared_templates/register/ directory
# containing templates for each auth view.
# import project or app that the accounts link to as below. 
from orders import views as main
from django.urls import path
from . import views

app_name='users'
urlpatterns = [
    # registration page
    path('register/', views.registerUser, name='register'),
    
    # account settings
    path('settings/', views.settings, name='settings'),
    
    # /link to main app's index
    path(r'', main.index, name='index'),
]
