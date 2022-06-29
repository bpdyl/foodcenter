from django import template
from apps.restaurants.models import Restaurant

register = template.Library()

@register.filter(name='split')
def split(str, key):
    return str.split(key)

@register.filter(name='multiply')
def multiply(value,arg):
	return value * arg

@register.filter(name='remfl')
def remfl(str1, key):
	if str1 != '' and key != '':
		return str(str1)[int(key):-int(key)]

@register.filter(name='product')
def product(str1, key):
	if str1.split(key)[0] != '':
		ppp = Restaurant.objects.filter(product_id=str1.split(key)[0]).first()
		return [ppp.rest_name,ppp.rest_photo.url,ppp.rest_phone]
