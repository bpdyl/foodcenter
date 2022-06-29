from django.db import models
from django.contrib.auth.models import User
from apps.restaurants.models import Restaurant
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from PIL import Image
# Create your models here.

class UserDetail(models.Model):
	GENDER_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True, related_name='customer')
	photo = models.ImageField(default='user_photos/nouser.jpg',upload_to='user_photos')
	phone = PhoneNumberField(null=True)
	gender = models.CharField(max_length=6,choices=GENDER_CHOICES, null=True)
        
	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)

		img = Image.open(self.photo.path)
		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.photo.path)
	def __str__(self):
		return self.user.first_name + " "+self.user.last_name +" "+self.user.email

class Cart(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='cart')
	food_id = models.CharField(max_length=100)
	restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, null=True)
	number = models.PositiveIntegerField(default=0)


class Contact(models.Model):
	date = models.DateField(auto_now=True)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	subject = models.CharField(max_length=100)
	message = models.TextField()
	
	def __str__(self):
		return self.email

class Address(models.Model):
	STATE_CHOICES = (
	("Bagmati",'Bagmati'),
	)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='address')
	alternate_phone = PhoneNumberField(null=True,blank=True)
	street_address = models.TextField()
	zipcode = models.CharField(max_length=6, null=True)
	area = models.CharField(max_length=100, null=True, blank=True)
	city = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
	default = models.BooleanField(default=False)

	def __str__(self):
		return self.street_address +" , "+self.area