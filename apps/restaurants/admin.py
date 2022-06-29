from django.contrib import admin
from .models import *
# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('rest_name',)}
    list_display = ('rest_name','rest_phone','rest_Address','status','is_verified','rest_reg_date','user')
    list_filter = ('rest_name','rest_phone','rest_Address','status','is_verified','rest_reg_date','user')

class restFoodModelAdmin(admin.ModelAdmin):
    model = restFoodModel
    list_display = ('food_name','restaurant', 'menu', 'food_id','food_price','id','food_image')
    list_filter = ('restaurant', 'menu__menu_name', 'food_id','food_name','food_price',)

class restMenuModelAdmin(admin.ModelAdmin):
    model = restMenuModel
    list_display =('menu_name','restaurant','menu_description','id','get_food')
    list_filter = ('menu_name','restaurant','menu_description','id',)
    def get_food(self,obj):
       foods = restFoodModel.objects.filter(menu__menu_name = obj.menu_name, restaurant = obj.restaurant)
       food_list = [f.food_name for f in foods]
       return food_list
    get_food.short_description = 'Foods'

class featuredAdmin(admin.ModelAdmin):
    model = featured
    list_display =('restaurant','number','id')
    list_filter =('restaurant','number')

class OrderAdmin(admin.ModelAdmin):
    model = Orders
    list_display = ('order_id','user','get_orderitem','get_restaurant','amount','shipping_address','status','ordered_date',)
    def get_orderitem(self,obj):
        items = OrderItem.objects.filter(user = obj.user, order__order_id = obj.order_id)
        item_list = [f.food_item.food_name for f in items]
        return item_list
    def get_restaurant(self,obj):
        rest = OrderItem.objects.filter(user = obj.user,order__order_id = obj.order_id)
        for f in rest:
            return f.restaurant.rest_name
    get_restaurant.short_description = 'Restaurant'
    get_orderitem.short_description = 'Ordered Items'

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ('food_item','order','user','restaurant','price','quantity','restaurant_paid')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(restMenuModel, restMenuModelAdmin)
admin.site.register(restFoodModel, restFoodModelAdmin)
admin.site.register(featured, featuredAdmin)
admin.site.register(Orders,OrderAdmin)
admin.site.register(OrderItem,OrderItemAdmin)
