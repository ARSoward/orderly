from .models import Business, Product
from django.db.models import Q
from ajax_select import register, LookupChannel

@register('business')
class BusinessLookup(LookupChannel):
    model = Business
    def get_query(self, q, request):
        return Business.objects.filter(business_name__icontains=q)
        
@register('product')
class ProductLookup(LookupChannel):
    model = Product
    def get_query(self, q, request): #grab business_id from request to filter
        return Product.objects.filter(
          Q(name__icontains=q) | Q(description__icontains=q)
        )
          
