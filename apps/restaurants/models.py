from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from PIL import Image
import datetime
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
import apps.core.models 

def get_display(key, list):
    d = dict(list)
    if key in d:
        return d[key]
    return "Pending"

class Restaurant(models.Model):
        class RestaurantObjects(models.Manager):
            def get_queryset(self):
                return super().get_queryset() .filter(is_verified=True)

	# GENDER_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
        STATE_CHOICES = (
            ("Bagmati",'Bagmati'),
            )
        options = (
            ('closed','Close'),
            ('open','Open'),
        )
        user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='restaurant', on_delete=models.CASCADE)
        rest_name = models.CharField(max_length=500,null=True)
        rest_photo = models.ImageField(default='user_photos/nouser.jpg',upload_to='user_photos')
        rest_phone = PhoneNumberField(null=True)
        alternate_phone = PhoneNumberField(null=True,blank=True)
        rest_Address = models.CharField(max_length=250)
        zipcode = models.CharField(max_length=6, null=True)
        rest_area = models.CharField(max_length=100, null=True, blank=True)
        city = models.CharField(max_length=100, null=True, blank=True)
        state = models.CharField(max_length=50,choices=STATE_CHOICES, null=True)
        rest_opentime = models.TimeField(null = True, blank = True)
        rest_closetime = models.TimeField(null = True, blank = True)
        status = models.CharField(max_length=10,choices = options, default = 'open')
        slug = models.SlugField(max_length = 250, unique_for_date ='rest_reg_date')
        rest_description = models.TextField(null=True,blank = True)
        account_Holder_Name = models.CharField(max_length=50, null=True)
        account_Number = models.CharField(max_length=20, null=True)
        rest_merchant_id = models.IntegerField(null = True, blank = True)
        rest_reg_date = models.DateTimeField(auto_now_add = True)
        is_verified = models.BooleanField(default=False)
        objects = models.Manager() #default manager
        restobjects = RestaurantObjects() #custom manger
        class Meta:
            ordering = ('rest_reg_date',)

        def __str__(self):
            return self.rest_name

        def save(self, *args, **kwargs):
            if not self.id:
                self.slug = slugify(self, self.rest_name)
            super(Restaurant, self).save(*args, **kwargs)

            # img = Image.open(self.photo.path)
            # if img.height > 300 or img.width > 300:
            #     output_size = (300, 300)
            #     img.thumbnail(output_size)
            #     img.save(self.photo.path)
        @property
        def check_time(self):
            now = datetime.datetime.now().time()
            print(now)
            if self.rest_opentime <=now <=self.rest_closetime:
                return True
            else:
                return False

class restMenuModel(models.Model):
    restaurant = models.ForeignKey(Restaurant,null = True, on_delete = models.CASCADE,related_name='menu')
    menu_name = models.CharField(max_length = 50)
    menu_description = models.TextField(max_length=1000,null=True,blank=True)

    def __str__(self):
        return self.menu_name + " " + str(self.restaurant)

    @property
    def get_fooditems(self):
        return restFoodModel.objects.filter(menu__menu_name = self.menu_name, restaurant = self.restaurant)

class restFoodModel(models.Model):
    restaurant = models.ForeignKey(Restaurant,null = True, on_delete = models.CASCADE,related_name='foods')
    menu = models.ForeignKey(restMenuModel,null = True, on_delete = models.CASCADE,related_name = 'foodmenu')
    food_id = models.CharField(max_length=100,default='')
    food_name = models.CharField(max_length = 200)
    slug = models.SlugField(db_index=False,null = True)
    food_image = models.ImageField(upload_to='foods/images',default='foods/images/default.png', null = True, blank = True)
    food_description = models.CharField(max_length = 10000, null = True, blank = True)
    food_price = models.PositiveIntegerField()

    class Meta:
        unique_together = (('slug','menu','restaurant'),)

    def save(self, *args, **kwargs):
            if not self.id:
                self.slug = slugify(self.food_name)+"-"+slugify(self.restaurant)
            super().save(*args, **kwargs)

            img1 = Image.open(self.food_image.path)
            if img1.height > 1500 or img1.width > 1500:
                output_size = (1500, 1500)
                img1.thumbnail(output_size)
                img1.save(self.food_image.path)


    def __str__(self):
        return self.food_name + "  " + str(self.menu.menu_name) + " " + str(self.restaurant)

class featured(models.Model):
    restaurant = models.OneToOneField(Restaurant,default="",related_name="featured",on_delete=models.CASCADE,null=True)
    number = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.restaurant}'

    class Meta:
        verbose_name_plural = 'Featured'


class Orders(models.Model):
    STATUS_CHOICES = (("Accepted",'Accepted'),("Packed",'Packed'),("On The Way",'On The Way'),("Delivered",'Delivered'),("Cancelled",'Cancelled'))
    order_id = models.CharField(max_length=50,default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE, related_name='customers')
    amount = models.IntegerField(default = 0)
    shipping_address = models.ForeignKey("core.Address", on_delete = models.SET_NULL, null=True,blank=True)
    status = models.CharField(max_length=15,choices=STATUS_CHOICES,default='Pending')
    ordered_date = models.DateTimeField(auto_now_add=True,auto_now = False)

    def __str__(self):
        return f'{self.user.first_name}' + " " +str(self.order_id)
    @property
    def get_status(self):
        return get_display(self.status,self.STATUS_CHOICES)

    def get_subtotal(self):
        total = 0
        order_items = OrderItem.objects.filter(user = self.user, order__order_id = self.order_id)
        for item in order_items:
            total += item.get_total_item_price()
        return total
    @property
    def get_item_restaurant(self):
        item_rest = OrderItem.objects.filter(order__order_id = self.order_id)
        for rest in item_rest:
            return rest.restaurant.rest_name
    def whenordered(self):
        now = timezone.now()
        
        diff= now - self.ordered_date

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds= diff.seconds
            
            if seconds == 1:
                return str(seconds) +  "second ago"
            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
            minutes= math.floor(diff.seconds/60)

            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
            hours= math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if diff.days >= 1 and diff.days < 30:
            days= diff.days
        
            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if diff.days >= 30 and diff.days < 365:
            months= math.floor(diff.days/30)
            

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years= math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

class OrderItem(models.Model):
    user = user = models.ForeignKey(settings.AUTH_USER_MODEL, default='', on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, related_name = 'items',on_delete = models.CASCADE)
    food_item = models.ForeignKey(restFoodModel, related_name='items',on_delete = models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, related_name='items',on_delete=models.CASCADE)
    restaurant_paid = models.BooleanField(default=False)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.user)+" "+ str(self.order.order_id)
        
    def get_total_item_price(self):
        return self.quantity * self.price