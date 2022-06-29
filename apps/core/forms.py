from django import forms
from django.contrib.auth.models import User
from apps.users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.core.exceptions import ValidationError
from .models import UserDetail,Address

class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control custom-class'}))
	last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control custom-class'}))
	email = forms.CharField(label=("Email"),widget=forms.TextInput(attrs={'class':'form-control custom-class','oninput':'validate()'}))
	phone = PhoneNumberField(label=("Phone"),widget=forms.NumberInput(attrs={'class':'form-control custom-class'}))
	password1 = forms.CharField(label=("Password"), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control custom-class'}),)
	password2  = forms.CharField(label=("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'class':'form-control custom-class'}),)
	class Meta:
		model = CustomUser
		fields = ['first_name', 'last_name', 'email','phone', 'password1', 'password2']

	def clean(self):
		cleaned_data = super(UserRegisterForm,self).clean()
		password1 = cleaned_data.get("password1")
		password2 = cleaned_data.get("password2")

		if password1!= password2:
			raise forms.ValidationError("Password and Confirm Password fields did not match")

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = [
			'first_name',
			 'last_name',
			 'email',
		]

class UpdateUserDetailForm(forms.ModelForm):
	class Meta:
		model = UserDetail
		fields = [
			'photo',
			'phone',
			'gender',
		]

class UserAddressForm1(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = [
			'first_name',
			 'last_name',
		]
class UserAddressForm(forms.ModelForm):
	STATE_CHOICES = (
		('',"Select State"),
	("Bagmati",'Bagmati'),
	)
	address = forms.CharField(error_messages = {'required':'Enter your address'})
	area = forms.CharField(error_messages = {'required':'Enter your area'})
	city = forms.CharField(error_messages = {'required':'Enter your city'})
	zipcode = forms.CharField(error_messages = {'required':'Enter your zipcode'})
	alternate_phone = PhoneNumberField(widget=forms.NumberInput(attrs={'placeholder':'Alternate Phone (optional)'}), required = False)
	state = forms.CharField(widget=forms.Select(attrs={},choices = STATE_CHOICES))
	set_default_address = forms.BooleanField(required=False)
	use_default_address = forms.BooleanField(required = False)
	class Meta:
		model = Address
		fields = [
			'address',
			'area',
			'city',
			'zipcode',
			'alternate_phone',
			'state',
		]