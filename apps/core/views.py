from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UpdateUserDetailForm, UserUpdateForm, UserAddressForm, UserAddressForm1
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from apps.restaurants.models import (Restaurant, restFoodModel,restMenuModel,featured,Orders,OrderItem)
from .models import *
from django.conf import settings
import json
import stripe
from apps.users.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash , logout
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.urls import reverse
# Create your views here.

delivery_charge = 100
def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

def index(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    rest = Restaurant.restobjects.all()
    featured_rest = featured.objects.filter(restaurant__in = rest).order_by('-number')[0:10]
    cart_element_no = len([p for p in Cart.objects.all() if p.user == request.user])
    params = {
        'featured': featured_rest,
        'cart_element_no':cart_element_no,
        'rest':rest,
    }

    return render(request,'core/home.html',params)
@login_required
def cart(request,rest_id):
    if request.user.is_authenticated:
        allfoods = []
        subtotal = 0
        delivery_charge = 100
        cart_items = [f for f in Cart.objects.all() if f.user == request.user]
        for item in cart_items:
            tempTotal = item.number * restFoodModel.objects.filter(id=f.id)[0].price
            subtotal += tempTotal
        
        for c in cart_items:
            food = restFoodModel.objects.filter(id=c.id)[0]
            allfoods.append([c,food])
        context = {
                'allfoods':allfoods,
                'cart_element_no': len([p for p in Cart.objects.all() if p.user == request.user]),
                'total':subtotal+delivery_charge
        }
@login_required
def my_order(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    STATUS_CHOICES = (("Accepted",'Accepted'),("Packed",'Packed'),("On The Way",'On The Way'),("Delivered",'Delivered'),("Cancelled",'Cancelled'))
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        o = Orders.objects.filter(order_id=order_id)[0]
        o.status = 'Cancel'
        o.save()
    customer_orders = Orders.objects.filter(user = request.user).order_by('-ordered_date')
    context = {
        'orders':customer_orders,
        'title':"My orders",
        'status_choices':STATUS_CHOICES,
    }
    # params = {
    #     'orders': [i for i in Orders.objects.all() if i.user == request.user and i.status != 'Delivered' and i.status != 'Cancel'],
    #     'delivered': [i for i in Orders.objects.all() if i.user == request.user and i.status == 'Delivered'],
    #     'cancel': [i for i in Orders.objects.all() if i.user == request.user and i.status == 'Cancel'],

    # }
    return render(request,'core/myorders.html', context)

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                usr = CustomUser.objects.filter(email=email).first()
                usr.email = email
                usr.phone = phone
                usr.save()
                UserDetail(user=usr).save()
                messages.success(request, f'Account is Created for {usr.first_name}')
                return redirect('login')
        else:
            form = UserRegisterForm()
    return render(request, 'core/signup.html',{'form':form, 'title':'Sign Up'})

@login_required
def account_settings(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    if request.method == 'POST':
        #User Details Update
        s_form = UpdateUserDetailForm(request.POST, request.FILES, instance=request.user.customr)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if s_form.is_valid() and u_form.is_valid():
            s_form.save()
            u_form.save()
            messages.success(request, f'Your Account has been Updated!')
            return redirect("account_settings")

        #Change Password
        pass_change_form = PasswordChangeForm(request.user, request.POST)
        if pass_change_form.is_valid():
            user = pass_change_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account_settings')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        s_form = UpdateUserDetailForm(instance=request.user.customer)
        u_form = UserUpdateForm(instance=request.user)
        pass_change_form = PasswordChangeForm(request.user)
    detl = {
        'u_form':u_form,
        's_form':s_form,
        'pass_change_form':pass_change_form,
        'title':'User Account Settings',
        'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
        }
    return render(request, 'main/account_settings.html', detl)


def view_all(request,feat):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    if feat=='featured':
        print('This is featured restaurant page')
        rest = Restaurant.restobjects.all()
        context = {
            'featured':[i for i in featured.objects.filter(restaurant__in = rest)[::-1]],
            'feat':'Featured Restaurants',
            'cart_element_no':len([p for p in Cart.objects.all() if p.user == request.user])
        }
        return render(request,'core/view_featured.html',context)
    elif feat=='index':
        print('this is view all function')
        all_rest = Restaurant.restobjects.all()
        context = {
            'all_rest':all_rest,
            'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
        }
        return render(request,'core/view_all.html',context)

def view_detail(request,rest_id):
    rest = Restaurant.objects.get(pk = rest_id)
    menulist = restMenuModel.objects.filter(restaurant = rest)
    foodlist = restFoodModel.objects.filter(restaurant = rest)
    if request.user.is_authenticated:
        allfoods = []
        subtotal = 0
        delivery_charge = 100
        cart_items = [f for f in Cart.objects.all() if f.user == request.user]
        for f in cart_items:
            if f.number <= 0:
                cart_items.remove(f)
        for item in cart_items:
            tempTotal = item.number * restFoodModel.objects.filter(id=item.food_id).first().food_price
            subtotal += tempTotal
        
        for c in cart_items:
            food = restFoodModel.objects.filter(id=c.food_id).first()
            allfoods.append([c,food])
        service_charge = 0.1*subtotal  
        context = {
            'menulist':menulist,
            'restaurant':rest,
            'cart_element_no':len([p for p in Cart.objects.all() if p.user == request.user]),
            'allfoods':allfoods,
            'subtotal':subtotal,
            'total':subtotal+delivery_charge,
            'delivery_charge':delivery_charge,
        }
        return render(request,'core/view_detail.html',context)
    context = {
        'menulist':menulist,
        'restaurant':rest,
        'cart_element_no':len([p for p in Cart.objects.all() if p.user == request.user])
    }
    return render(request,'core/view_detail.html',context)

def search(request):
    query = request.GET.get('query')
    if not query:
        print('empty inserted')
        all_rest = Restaurant.restobjects.all()
        context = {
            'heading':'Available Restaurants',
            'all_rest':all_rest,
            'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
        }
        return render(request,'core/view_all.html',context)
    else:
        results = Restaurant.restobjects.filter(
            Q(rest_name__icontains=query) | Q(rest_Address__icontains =query) | Q(rest_area__icontains = query) | Q(rest_description__icontains = query)| Q(menu__menu_name__icontains = query) | Q(foods__food_name__icontains = query)).distinct()
        print(results)
        context = {
            'heading':'Search Results',
            'restaurant':results,
            'cart_element_no' : len([p for p in Cart.objects.all() if p.user == request.user]),
        }
        return render(request,'core/view_all.html',context)
@login_required
def addToCart(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    cart_items = [c for c in Cart.objects.all() if c.user == request.user]
    cart_items_id = [i.food_id for i in cart_items]
    if request.method == 'GET':
        foodId = request.GET['foodId']
        f_price = restFoodModel.objects.get(id = foodId).food_price
        restId = request.GET['restId']
        food = restFoodModel.objects.get(id=foodId)
        subtotal = 0
        delivery_charge = 100
        for i in cart_items:
            if i.restaurant.id == int(restId):
                for item in cart_items:
                    if foodId == item.food_id:
                        item.number += 1
                        print("Item save garnu vanda agadi"+str(item.number))
                        item.save()
                        new_cart_items = [f for f in Cart.objects.all() if f.user == request.user]
                        print(new_cart_items)
                        for new_item in new_cart_items:
                            tempTotal = new_item.number * restFoodModel.objects.filter(id = new_item.food_id).first().food_price
                            subtotal += tempTotal
                        print("Ma chai yo subtotal ho hai "+str(subtotal)+" ani id"+str(item.id))
                        f_name = restFoodModel.objects.get(id = foodId).food_name
                        print("HEllo this is me "+str(f_name))
                        data = {
                            # 'cart_data':cart_data,
                            'num':Cart.objects.get(id=item.id).number,
                            'cart_count':len(cart_items),
                            'subtotal':subtotal,
                            'total':subtotal+delivery_charge,
                        }
                        return JsonResponse(data)
                        return HttpResponse(len(cart_items))
                cart = Cart(user = request.user, food_id = foodId,restaurant=food.restaurant,number=1)
                cart.save()
                print("ma yaha chu")
                new_cart_items = Cart.objects.filter(user = request.user).values()
                cart_data = list(new_cart_items)
                for c in cart_data:
                    print("yo ma ho "+str(c["number"]))
                datas = {
                    'num':Cart.objects.get(id=cart.id).number,
                    'cart_data':cart_data,
                    'cart_count':len(cart_items)+1,
                    'subtotal':subtotal,
                    'delivery_charge':delivery_charge,
                    'total':subtotal+delivery_charge,
                        }
                return JsonResponse(datas)
            else:
                return JsonResponse({'status':0})
        cart = Cart(user = request.user, food_id = foodId,restaurant=food.restaurant,number=1)
        cart.save()
        print(cart)
        new_cart_items = Cart.objects.filter(user = request.user).values()
        cart_data = list(new_cart_items)
        cart_items2 = [f for f in Cart.objects.all() if f.user == request.user]

        subtotal = f_price
        print("yo chai naya baneko cartko id "+str(cart.id))
        datas = {
            'num':Cart.objects.get(id=cart.id).number,
            'cart_data':cart_data,
            'cart_count':len(cart_items)+1,
            'subtotal':subtotal,
            'delivery_charge':delivery_charge,
            'total':subtotal+delivery_charge,
            }
        return JsonResponse(datas)  
    else:
        return HttpResponse("")
    # data = json.loads(request.body)
    # foodId = data['foodId']
    # action = data['action']
    # print('Action:',action) 
    # print('Food:',foodId)

    # user = request.user
    # food = restFoodModel.objects.get(id=foodId)
    # cart, created = Cart.objects.get_or_create(user = user,food_id=food.id,restaurant=food.restaurant)

    # if action == 'add':
    #     cart.number = (cart.number + 1)
    # elif action == 'remove':
    #     cart.number = (cart.number -1)
    # cart.save()

    # if cart.number<=0:
    #     cart.delete()
    # return JsonResponse('Item was added', safe=False)

@login_required
@csrf_exempt
def reset_cart(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    data = json.loads(request.body)
    restId = data['restId']
    cart = Cart.objects.filter(user = request.user)
    cart.delete()
    addToCart(request)
    return JsonResponse({'status':'removed'})

@login_required
def update_cart_item(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    if request.method == 'GET':
        foodId = request.GET['foodId']
        cartfoodId = request.GET['cartfoodid']
        action = request.GET['action']
        f_price = restFoodModel.objects.get(id = cartfoodId).food_price
        cart = Cart.objects.get(id=foodId)
        if action == 'plus':
            cart.number+=1
        elif action == 'minus':
            cart.number-=1
        cart.save()
        if cart.number<=0:
            cart.delete()
        subtotal = 0
        delivery_charge = 100
        cart_items2 = [f for f in Cart.objects.all() if f.user == request.user]
        for item in cart_items2:
            tempTotal = item.number * restFoodModel.objects.filter(id=item.food_id).first().food_price
            subtotal += tempTotal

        datas = {
            'num':Cart.objects.get(id=foodId).number,
            'food_price':f_price,
            'subtotal':subtotal,
            'delivery_charge':delivery_charge,
            'total':subtotal+delivery_charge,
        }
        return JsonResponse(datas)
    else:
        return HttpResponse("")
        
@login_required
def delete_cart_item(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    if request.method == 'GET':
        foodId = request.GET['foodId']
        cart = Cart.objects.get(id = foodId)
        cart.delete()
        subtotal = 0
        delivery_charge = 100
        cart_items2 = [p for p in Cart.objects.all() if p.user == request.user]
        for item in cart_items2:
            tempTotal = item.number * restFoodModel.objects.filter(id = item.food_id).first().food_price
            subtotal += tempTotal

        datas = {
            'cart_count':len(cart_items2),
            'delivery_charge':delivery_charge,
            'subtotal':subtotal,
            'total':subtotal+delivery_charge,
        }
        return JsonResponse(datas)
    else:
        return HttpResponse("")

@login_required        
def checkout(request):
    if request.user.is_staff:
        return redirect('dashboard')
    else:
        pass
    temp = 0
    cart_subtotal = 0
    delivery_charge = 100
    allfoods = []
    cart_items = [p for p in Cart.objects.all() if p.user == request.user]
    for cart in cart_items:
        food = restFoodModel.objects.filter(id = cart.food_id).first()
        tempTotal = cart.number * food.food_price
        cart_subtotal += tempTotal
        allfoods.append([cart,food])
    print(cart_subtotal)
    if request.method == "POST":
        address_form = UserAddressForm(request.POST)
        print("i am here")
        if address_form.is_valid():
            if Orders.objects.all().last():
                order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
            else:
                order_id = 'ordr001'
            order = Orders.objects.create(order_id = order_id,user=request.user)
            use_default_address = address_form.cleaned_data.get('use_default_address')
            if use_default_address:
                print("Using the default address")
                deliv_address = Address.objects.filter(user = request.user, default = True)
                if deliv_address.exists():
                    delivery_address = deliv_address[0]
                    order.shipping_address = delivery_address
                    order.save()
                else:
                    messages.info(request,"No default delivery address available")
                    return redirect('checkout')
            else:
                print("New delivery address")
                shipping_address = address_form.cleaned_data.get('address')
                area = address_form.cleaned_data.get('area')
                city = address_form.cleaned_data.get('city')
                zipcode = address_form.cleaned_data.get('zipcode')
                state = address_form.cleaned_data.get('state')
                alternate_phone = address_form.cleaned_data.get('alternate_phone')

                if is_valid_form([shipping_address, area, city, zipcode, alternate_phone]):
                    shipping_address = Address(
                        user = request.user,
                        alternate_phone = alternate_phone,
                        street_address = shipping_address,
                        zipcode = zipcode,
                        area = area,
                        city = city,
                        state = state
                    )
                    shipping_address.save()
                    order.shipping_address = shipping_address
                    order.save()

                    set_default_address = address_form.cleaned_data.get('set_default_address')
                    if set_default_address:
                        shipping_address.default = True
                        shipping_address.save()
                else:
                    messages.info(request,"Please fill in the required delivery address")
            pay_mode = request.POST.get('pay_mode')
            if pay_mode == 'on':
                for item in cart_items:
                    print("cash on delivery")
                    food = restFoodModel.objects.filter(id=item.food_id).first()
                    OrderItem.objects.create(
                        user = request.user,
                        order = order,
                        food_item = food,
                        restaurant = item.restaurant,
                        price = food.food_price,
                        quantity = item.number
                    )
                    item.delete()
                subtotal = order.get_subtotal()
                order.amount = subtotal
                order.save()
                return redirect('/myorders')
            else:
                temp = 1
                print("payment gateway")
        else:
            print("i am invalid")
    else:
        
        address_form = UserAddressForm()
    if temp == 1:
        print("and now payment continuing")
        o_id = ''
        for item in cart_items:
            food = restFoodModel.objects.filter(id=item.food_id).first()
            OrderItem.objects.create(
                user = request.user,
                order = order,
                food_item = food,
                restaurant = item.restaurant,
                price = food.food_price,
                quantity = item.number
            )
            subtotal = order.get_subtotal()
            order.amount = subtotal
            order.save()
            stripe.api_key = settings.STRIPE_SECRET_KEY
            customer = stripe.Customer.create(
                email = request.user.email,
                source = request.POST['stripeToken']
            )
            charge = stripe.Charge.create(
                customer = customer,
                amount = (subtotal+delivery_charge) * 100,
                currency = 'inr',
                description = 'Charge from foodcenter',
            )
            print(charge)
            item.delete()
    context = {
        'allfoods':allfoods,
        'cart_element_no':len(cart_items),
        'address_form':address_form,
        'subtotal':cart_subtotal,
        'delivery_charge':delivery_charge,
        'total':cart_subtotal+delivery_charge,
        'cart_count':len(cart_items),
        'stripe_pub_key':settings.STRIPE_PUB_KEY
        # 'cart_rest':cart_rest,
    }
    default_delivery_address = Address.objects.filter(
        user = request.user,
        default=True
    )
    if default_delivery_address.exists():
        context.update(
            {'default_address':default_delivery_address[0]}
        )
    return render(request,'core/new_checkout.html',context) 


                    

# @login_required
# def checkout(request):
#     if request.user.is_staff:
#         return redirect('dashboard')
#     else:
#         pass
#     temp = 0
#     allfoods = []
#     cart_items = [p for p in Cart.objects.all() if p.user == request.user]
#     for item in cart_items:
#         print("i am quantity")
#         print(item.number)
#         print("I am cart restaurant")
#         print(type(item.restaurant))
#         food = restFoodModel.objects.filter(id=item.food_id).first()
#         print("i am food restaurant")
#         print(type(food.restaurant))
#         print("i am food")
#         print(food.food_price)
#         allfoods.append([item, food])
#     if request.method == 'POST':
#         address_form = UserAddressForm(request.POST, instance=request.user.customer)
#         u_form2 = UserAddressForm1(request.POST, instance=request.user)
#         if address_form.is_valid() and u_form2.is_valid():
#             address_form.save()
#             u_form2.save()
#             pay_mode = request.POST.get('pay_mode')
#             if pay_mode == 'on':
#                 subtotal = 0
#                 delivery_charge = 100
#                 for p in cart_items:
#                     tempTotal = p.number * restFoodModel.objects.filter(id=p.food_id).first().food_price
#                     subtotal += tempTotal
#                     total = subtotal+delivery_charge
#                 print("I am here and this is the total"+str(total))
#                 for i in cart_items:
#                     if Orders.objects.all().last():
#                         order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
#                     else:
#                         order_id = 'ordr001'
#                     food1 = i.food_id+'|'+str(i.number)+','
#                     cart_rest = restFoodModel.objects.filter(id=i.food_id).first().restaurant
#                     Orders(order_id=order_id,user=request.user,restaurant=cart_rest,foods=food1,amount = total).save()
#                     i.delete()
#                 return redirect('/myorders')
#             else:
#                 temp = 1
#     else:
#         address_form = UserAddressForm(instance=request.user.customer)
#         u_form2 = UserAddressForm1(instance=request.user)
#     subtotal = 0
#     delivery_charge = 100
#     for p in cart_items:
#         tempTotal = p.number * restFoodModel.objects.filter(id=p.food_id).first().food_price
#         subtotal += tempTotal
#     total = subtotal+delivery_charge

#     if temp == 1:
#         o_id = ''
#         for i in cart_items:
#             order_id = 'ordr'+str((Orders.objects.all().last().pk)+1)
#             o_id = order_id
#             food1 = i.food_id+'|'+str(i.number)+','
#             cart_rest = restFoodModel.objects.filter(id=i.food_id).first().restaurant
#             Orders(order_id=order_id,user = request.user,restaurant = cart_rest,foods = food1,amount=total)
#             print(total)
#             stripe.api_key = settings.STRIPE_SECRET_KEY
#             customer = stripe.Customer.create(
#                 email = request.user.email,
#                 source = request.POST['stripeToken']
#             )
#             charge = stripe.Charge.create(
#                 customer = customer,
#                 amount = total * 100,
#                 currency = 'inr',
#                 description = 'Charge from foodcenter',
#             )
#             print(charge)

#     context = {
#         'allfoods':allfoods,
#         'cart_element_no':len(cart_items),
#         'address_form':address_form,
#         'u_form':u_form2,
#         'total':subtotal+delivery_charge,
#         'stripe_pub_key':settings.STRIPE_PUB_KEY
#         # 'cart_rest':cart_rest,
#     }
#     return render(request,'core/checkout.html',context)

def page_not_found(request,exception):
    return render(request,'core/404.html')    

def contact(request):
    return render(request,'core/contact.html')