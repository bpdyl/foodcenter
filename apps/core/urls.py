from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='home'),
    path('register/', views.register, name="signup"),
    path('cart/', views.cart, name="main_cart"),
    path('contact/',views.contact, name='contact'),
    path("restaurant/<str:feat>", views.view_all, name="restaurants_view_all"),
    path("restaurant/detail/<int:rest_id>", views.view_detail, name ="view_detail"),
    path("search/index",views.search,name = "rest_search"),
    path('add_to_cart/',views.addToCart,name="add-to-cart"),
    path('update_cart_item/',views.update_cart_item,name = 'update-cart-item'),
    path('reset_cart/',views.reset_cart,name = 'reset-cart'),
    path('remove_cart_item/',views.delete_cart_item,name = 'delete-cart-item'),
    path('checkout/',views.checkout,name = 'core_checkout'),
    path('manage/profile/', views.account_settings, name="account_settings"),
    path('manage/myorders',views.my_order,name="myorders"),
]