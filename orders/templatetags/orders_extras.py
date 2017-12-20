from django import template
register = template.Library()

@register.filter(name='addCSS')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})
