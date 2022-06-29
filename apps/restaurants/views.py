from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import *
from apps.users.models import CustomUser
from django.template.loader import render_to_string
from django import forms
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from .forms import (RestaurantRegisterForm, RestaurantAddressForm, UpdateRestaurantDetailForm, UpdateRestaurantAccountDetailForm, 
MenuForm,MenuUpdateForm ,FoodForm,FoodUpdateForm)
from apps.core.forms import UserUpdateForm
from django.contrib.auth.decorators import login_required
from math import ceil
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def restaurant_signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = RestaurantRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                restaurant_name = form.cleaned_data.get('restaurant_name')
                phone = form.cleaned_data.get('')
                usr = CustomUser.objects.filter(email=email).first()
                usr.is_staff=True
                usr.save()
                usr.email = email
                usr.save()
                restaurant = Restaurant.objects.create(user=usr,rest_name=restaurant_name,rest_phone=phone).save()
                messages.success(request,f'Account is created for {first_name}')
                return redirect('login')
        else:
            form = RestaurantRegisterForm()
            
    return render(request, 'restaurants/restaurant_signup.html',{'form':form,'title':'Become Restaurant Partner'})

def dashboard(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'GET':
            odrr = request.GET.get('odrr')
            st = request.GET.get('st')
            if st == 'Cancel':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'Cancel'
                o.save()
            if st == 'Accepted':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'Accepted'
                o.save()
            if st == 'Packed':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'Packed'
                o.save()
            if st == 'Delivered':
                o = Orders.objects.filter(order_id=odrr).first()
                o.status = 'On The Way'
                o.save()
        ordr = [i for i in Orders.objects.filter(restaurant=request.user.restaurant) if i.status != 'Cancel' and i.status != 'On The Way' and i.status != 'Delivered'][::-1]
        customer_count = 0
        rest_order = Orders.objects.filter(restaurant = request.user.restaurant)
        for u in rest_order:
            print(u.user.customer)
        print("it's order count"+str(rest_order))
        print("this is "+str(customer_count))
        params = {
                'orders':ordr,
                'dorders': [i for i in Orders.objects.filter(restaurant=request.user.restaurant) if i.status != 'Cancel' and i.status == 'On The Way' or i.status == 'Delivered'][::-1],
                # 'rest_order':order_count,

                }
        return render(request, 'restaurants/rest_dashboard.html', params)
    else:
        return redirect("/")

@login_required
def menu_list(request):
    if request.user.is_superuser or request.user.is_staff:
        restaurant = request.user.restaurant
        menu = [m for m in restMenuModel.objects.all() if m.restaurant == restaurant]
        context = {
            'menu_list':menu,
            "title":"Menu List",
        }
        return render(request,'restaurants/menu_list.html',context)
    else:
        messages.warning(request, f'Oh please you are not authorized !')
        return redirect("/")

@login_required
def food_list(request):
    if request.user.is_superuser or request.user.is_staff:
        restaurant = request.user.restaurant
        food = [f for f in restFoodModel.objects.all() if f.restaurant == restaurant]
        print(restaurant)
        context = {
            'restaurant':restaurant,
            'food_list':food,
            "title":"Food Item List",
        }
        return render(request,'restaurants/new_food_list.html',context)
    else:
        messages.warning(request, f'Oh please you are not authorized !')
        return redirect("/")

@login_required
def search_food(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method=='POST':
            search_str = json.loads(request.body).get('searchText')
            foods = restFoodModel.objects.filter(
                food_price__startswith=search_str, restaurant=request.user.restaurant) | restFoodModel.objects.filter(
                food_name__istartswith=search_str, restaurant=request.user.restaurant) | restFoodModel.objects.filter(
                food_description__icontains=search_str, restaurant=request.user.restaurant) | restFoodModel.objects.filter(
                menu__menu_name__istartswith=search_str, restaurant=request.user.restaurant)
            print(foods)    
            data = foods.values()
            return JsonResponse(list(data),safe=False)

@login_required
def add_food(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            form = FoodForm(request.POST, request.FILES,user = request.user)
            if form.is_valid():
                food = form.save(commit=False)
                food.restaurant = request.user.restaurant
                m = request.POST['menu']
                if m == "Select Menu":
                    messages.error(request,"Select a category")
                else:
                    food.menu = restMenuModel.objects.get(id = m)
                    # slug = slugify(fd_name)
                    if restFoodModel.objects.all():
                        food.food_id = 'food'+hex(restFoodModel.objects.all().last().id+1)
                    else:
                        food.food_id = 'food'+hex(0)
                    food.save()
                    messages.success(request, f'Food Item Added !')
                    return redirect('food_list')
        else:
            form = FoodForm(user=request.user)
        menu = restMenuModel.objects.filter(restaurant=request.user.restaurant)    
        context = {
            'form':form,
            'menu':menu,
            "title":"Add Food Item",
            "error":"Please select menu"

        }
        return render(request,'restaurants/add_food.html',context)
    else:
        messages.warning(request,f'Oh please you are not authorized !')
        return redirect('/')
        # food = [f for f in restFoodModel.objects.all() if f.restaurant == request.user.restaurant]

@login_required
def update_food(request,id):
    if request.user.is_superuser or request.user.is_staff:
        queryset = restFoodModel.objects.get(pk = id)
        if queryset.restaurant!=request.user.restaurant:
            messages.warning(request,f'Sorry you do not own this restaurant to perform this action')
            return redirect('/')
        form = FoodUpdateForm(user = request.user,instance=queryset)
        if request.method == 'POST':
            form = FoodUpdateForm(request.POST,request.FILES or None,instance=queryset,user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request,f'Updated successfully ! ')
                return redirect('food_list')
        menu = restMenuModel.objects.filter(restaurant=request.user.restaurant)
        context = {
            'form':form,
            'menu':menu,
            "title":"Edit Food Item Details",
            "foods":queryset
        }
        return render(request,'restaurants/add_food.html',context)
    else:
        messages.warning(request,f'Oh please you are not authorized')
        return redirect('/')

@login_required
def delete_food(request):
    if request.user.is_superuser or request.user.is_staff:
        foodId = request.POST.get('foodId')
        print(foodId)
        obj = restFoodModel.objects.get(pk = foodId)
        if obj.restaurant!=request.user.restaurant:
            messages.warning(request,f'Sorry you do not have permission to perform this action')
            return redirect('/')
        if request.method == 'POST':
            obj.delete()
            return JsonResponse({'status':1})
            messages.success(request,f'Deleted Successfully! ')
            return redirect('food_list')
        else:
            return JsonResponse({'status':0})
    else:
        messages.warning(request, f'Oh please you are not authorized !')
        return redirect("/")

@login_required
def add_menu(request):
    if request.user.is_superuser or request.user.is_staff:
        if request.method == 'POST':
            form = MenuForm(user=request.user,data =request.POST)
            if form.is_valid():
                menu = form.save(commit=False)
                menu.restaurant = request.user.restaurant
                print(menu.restaurant)
                menu.save()
                messages.success(request, f'Menu Added !')
                return redirect('menu_list')
        else:
            form = MenuForm(user = request.user)
        context = {
            'form':form,
            "title":"Add Menu",
        }
        return render(request, 'restaurants/add_menu.html',context)
    else:
        messages.warning(request, f'Oh please you are not authorized !')
        return redirect("/")





@login_required
def update_menu(request,id):
    if request.user.is_authenticated or request.user.is_staff:
        queryset = restMenuModel.objects.get(pk = id)
        if queryset.restaurant!=request.user.restaurant:
            messages.warning(request,f'Sorry you do not own this restaurant to perform this action')
            return redirect('menu_list')
        form = MenuUpdateForm(user = request.user,instance = queryset)
        if request.method == 'POST':
            form = MenuUpdateForm(request.POST,instance=queryset,user = request.user)
            if form.is_valid():
                form.save()
                messages.success(request,f'Updated Successfully! ')
                return redirect('menu_list')
        
        context = {
            'form':form,
            "title":"Edit Menu",
        }
        return render(request,'restaurants/add_menu.html',context)
    else:
        messages.warning(request, f'Oh please you are not authorized !')
        return redirect("/")

@login_required
def delete_menu(request,id):
    if request.user.is_superuser or request.user.is_staff:
        obj = restMenuModel.objects.get(pk = id)
        if obj.restaurant!=request.user.restaurant:
            messages.warning(request,f'Sorry you do not have permission to perform this action')
            return redirect('/')
        if request.method == 'POST':
            obj.delete()
            messages.success(request,f'Deleted Successfully! ')
            return redirect('menu_list')
        context = {'menu':obj}
        return render(request,'restaurants/menu_delete.html',context)
    else:
        messages.warning(request, f'Oh please you are not authorized !')
        return redirect("/")





	