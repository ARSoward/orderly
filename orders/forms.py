from django import forms
from datetime import date, timedelta
from .models import Order, OrderItem, Product, Business
from django_select2.forms import Select2Widget

#order form: 
# create new orders for a specific connection.
# display existing orders in a list.
class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    fields = ['requested_delivery', 'notes', ] # and standing order frequency 
    widgets = {'requested_delivery': forms.SelectDateWidget(),} #initial=date.today() + timedelta(days=7)
  #clean should check delivery against the business's settings
  
  #form must be saved with an Order instance that supplies the other fields:
  #order = Order(connection= , status = )
  #form = OrderForm(request.POST, instance=order)
  #form.save()
    
#orderItem form:
# create new items for a specific order.
# display existing items in a list.
class OrderItemForm(forms.ModelForm):
  class Meta:
    model = OrderItem
    fields = ['product', 'quantity',] #make it so product is only editable if it's a new orderItem
    widgets = {'product': Select2Widget}

#OrderItem Inline Formset Factory          
OrderItemSet = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, max_num=15, extra=1, can_delete=True)

    
#business form:
# vendors add new customers.

#product form:
# add new product for a specific vendor.
# display existing products in a list.

    
