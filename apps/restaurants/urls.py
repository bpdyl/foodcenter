from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
        path('dashboard/', views.dashboard, name = 'dashboard'),
		# path('home/', views.index, name = 'saler_home'),
        path('restaurant_signup/', views.restaurant_signup, name="restaurant_signup"),
    	# path('account_settings/', views.account_settings, name="saler_account_settings"),
        path('add-menu/',views.add_menu, name ='add_menu'),
		path('update-menu/<int:id>/', views.update_menu, name = 'edit_menu'),
        path('menu-list/',views.menu_list, name = 'menu_list'),
		path('delete-menu/<int:id>/',views.delete_menu, name='delete_menu'),
		path('add-food/',views.add_food,name = 'add_food'),
		path('update-food/<int:id>/',views.update_food, name = 'edit_food'),
		path('food-list/',views.food_list, name='food_list'),
		path('search-food',csrf_exempt(views.search_food),name='search_food'),
		path('delete-food/',views.delete_food,name='delete_food'),
    	# path('add_product/', views.add_product, name="add_product"),
    	# path('view_products/', views.view_products, name="view_products"),
    	# path('plus_element_cart/', views.plus_element_cart),
    	# path('minus_element_cart/', views.minus_element_cart),
    	# path('add_to_cart/', views.add_to_cart),
    	# path('delete_from_cart/', views.delete_from_cart),
        # path('cart/', views.mycart, name="cart"),
    	# path('MyOrders/', views.MyOrders, name="seller_orders"),
    	# path("products/<str:catg>", views.view_all, name="saler_products_view_all"),
    	# path("product/<int:prod_id>", views.productView, name="SalerProductView"),
    	# path("checkout/", views.checkout, name = "checkout")

	]