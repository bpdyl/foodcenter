from django.contrib import admin
from .models import *
from apps.restaurants.models import *

# Register your models here.
class UserDetailAdmin(admin.ModelAdmin):
    model = UserDetail
    list_display =('user','get_first_name','get_last_name','photo','phone','gender',)
    list_filter = ('gender',)

    def get_first_name(self,obj):
        return obj.user.first_name
    def get_last_name(self,obj):
        return obj.user.last_name
    get_first_name.short_description = "First Name"
    get_first_name.short_description = "Last Name"

class AddressAdmin(admin.ModelAdmin):
    model = Address
    list_display = ('user','street_address','alternate_phone','area','state','zipcode','city')

class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user','food_id','get_food_name','restaurant','number')
    list_filter = ('user','restaurant','id',)

    def get_food_name(self,obj):
        foods = restFoodModel.objects.filter(id = obj.food_id)
        food_list = [f.food_name for f in foods]
        return food_list
    get_food_name.short_description = "Foods"
admin.site.register(UserDetail,UserDetailAdmin)
admin.site.register(Cart,CartAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(Contact)