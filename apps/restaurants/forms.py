from .models import Restaurant, restFoodModel, restMenuModel
from django import forms
from django.contrib.auth.models import User
from apps.users.models import CustomUser
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

class RestaurantRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={}))
	email = forms.EmailField(label=("Email"),widget=forms.TextInput(attrs={'oninput':'validate()'}))
	restaurant_name = forms.CharField(label=("Company/Restaurant Name"),widget=forms.TextInput(attrs={}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={}),)
	password2  = forms.CharField(label=("Confirm"), strip=False, widget=forms.PasswordInput(attrs={}),)
	phone = PhoneNumberField(label=("Phone"),)
	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class RestaurantAddressForm(forms.ModelForm):
	rest_Address = forms.CharField(widget=forms.TextInput(attrs={}))
	rest_area = forms.CharField(required =True)
	city = forms.CharField(required =True)
	alternate_phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	rest_opentime = forms.TimeField()
	rest_closetime = forms.TimeField()
	class Meta:
		model = Restaurant
		fields = [
			'rest_phone',
			'rest_name',
			'alternate_phone',
			'rest_Address',
			'zipcode',
			'rest_area',
			'city',
			'state',
            'rest_opentime',
            'rest_closetime',
		]

class UpdateRestaurantDetailForm(forms.ModelForm):
	class Meta:
		model = Restaurant
		fields = [
			'rest_name',
			'rest_photo',
			'rest_name',
			'rest_phone',
			'alternate_phone',
			'rest_Address',
			'zipcode',
			'rest_area',
			'city',
			'state',
            'rest_opentime',
            'rest_closetime',
		]

class UpdateRestaurantAccountDetailForm(forms.ModelForm):
	class Meta:
		model = Restaurant
		fields = [
			'account_Holder_Name',
			'account_Number',
			'rest_merchant_id',
			]

class MenuForm(forms.ModelForm):
	class Meta:
		model = restMenuModel
		fields = ['menu_name','menu_description']
		labels ={
			'menu_name':'Name',
			'menu_description':'Description'
		}
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(MenuForm, self).__init__(*args,**kwargs)

	def clean_menu_name(self):#validate the menu name field
		menu_name = self.cleaned_data.get('menu_name')
		if(menu_name == ""):
			raise forms.ValidationError('This field cannot be left blank')
		if len(menu_name)<=2:
			raise forms.ValidationError('Menu name must have at least 3 characters')

		for instance in restMenuModel.objects.filter(restaurant=self.user.restaurant):
			if instance.menu_name.casefold() == menu_name.casefold():
				raise forms.ValidationError('Menu with the name '+ '"'+menu_name +'"' +' already exists. Please use another name')
		return menu_name

class MenuUpdateForm(forms.ModelForm):
	class Meta:
		model = restMenuModel
		fields = ['menu_name','menu_description']
		labels ={
			'menu_name':'Name',
			'menu_description':'Description'
		}
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(MenuUpdateForm, self).__init__(*args,**kwargs)

	def clean_menu_name(self):#validate the menu name field
		menu_name = self.cleaned_data.get('menu_name')
		if(menu_name == ""):
			raise forms.ValidationError('This field cannot be left blank')
		if len(menu_name)<=2:
			raise forms.ValidationError('Menu name must have at least 3 characters')

		return menu_name

class FoodForm(forms.ModelForm):
	class Meta:
		model = restFoodModel
		fields = '__all__'
		exclude = ['restaurant','slug','food_id','menu']
		labels ={
			'food_name':'Name',
			'food_description':'Description',
			'food_price':'Price',
			'food_image':'Food Image',

		}
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(FoodForm, self).__init__(*args,**kwargs)

	def clean_food_name(self):#validate the food name field
		food_name = self.cleaned_data.get('food_name')
		if(food_name == ""):
			raise forms.ValidationError('This field cannot be left blank')
		if len(food_name)<=2:
			raise forms.ValidationError('Food name must have at least 3 characters')

		for instance in restFoodModel.objects.filter(restaurant=self.user.restaurant):
			if instance.food_name.casefold() == food_name.casefold():
				raise forms.ValidationError('Food item with the name '+ '"'+food_name +'"' +' already exists. Please use another name')
		return food_name

	def clean_food_price(self):
		food_price = self.cleaned_data.get('food_price')
		if(food_price == ""):
			raise forms.ValidationError('This field cannot be left blank')
		if food_price<0:
			raise forms.ValidationError('Dhiraj sir le minus maa price nahalnu vannu vako cha')
		if food_price>5000:
			raise forms.ValidationError('Oh you are VIP restaurant owner. Sorry We cannot afford you')

		return food_price

class FoodUpdateForm(forms.ModelForm):
	class Meta:
		model = restFoodModel
		fields = '__all__'
		exclude = ['restaurant','slug','food_id']
		labels ={
			'menu':'Menu',
			'food_name':'Name',
			'food_description':'Description',
			'food_price':'Price',
			'food_image':'Food Image',
		}
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user')
		super(FoodUpdateForm, self).__init__(*args,**kwargs)

	def clean_food_name(self):#validate the food name field
		food_name = self.cleaned_data.get('food_name')
		if(food_name == ""):
			raise forms.ValidationError('This field cannot be left blank')
		if len(food_name)<=2:
			raise forms.ValidationError('Food name must have at least 3 characters')
		return food_name

	def clean_food_price(self):
		food_price = self.cleaned_data.get('food_price')
		if(food_price == ""):
			raise forms.ValidationError('This field cannot be left blank')
		if food_price<0:
			raise forms.ValidationError('Dhiraj sir le minus maa price nahalnu vannu vako cha')
		if food_price>5000:
			raise forms.ValidationError('Oh you are VIP restaurant owner. Sorry We cannot afford you')

		return food_price