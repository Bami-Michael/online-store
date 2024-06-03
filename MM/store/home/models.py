from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import random
from django.db.models.signals import post_save



CATEGORY_CHOICES = (
    ('Body product', 'Body Cream'),
    ('Makeup', 'Makeup'),
    ('Hair Product', 'Hair Product')
)




class Shipping_address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=50)    
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f"{self.user.username} {self.address}"
    



class Billing_address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=50)    
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Billing Address'

    def __str__(self):
        return f"{self.user.username} {self.address}"


class Contact(models.Model):
  name = models.CharField(max_length=254, null=True)
  email = models.EmailField(max_length=254, null=True)
  message = models.CharField(max_length=254, null=True)
  def __str__(self):
      return str(self.email)
   


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  accblock = models.CharField(max_length=254, default='open')  
  old_cart = models.CharField(max_length=254, blank=True, null=True)

  def __str__(self):
      return str(self.user.username)


#create a profile when a user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()

#automate profile creation with signals
post_save.connect(create_profile, sender=User)
  


class Item(models.Model):
    title = models.CharField(max_length=50)
    main_price = models.DecimalField(decimal_places=2, max_digits=6)
    discount_price = models.DecimalField(decimal_places=2, max_digits=6, blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='uploads/items/')

    def __str__(self):
        return self.title
    

    def price(self):
        if self.discount_price:
            price = self.discount_price
        else:
            price = self.main_price
        return price
    
    
    def discounted(self):
        if self.discount_price:
            x = self.main_price - self.discount_price
            y = (self.discount_price + self.main_price) / 2
            z = (x/y)*100
            return int(z)
        return 0




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=100)
    OrderItems = models.CharField(max_length=500)
    total = models.DecimalField(decimal_places=2, max_digits=6)
    payment_received = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    shipping_info = models.TextField()
    billing_info = models.TextField()

    def __str__(self):
        return f'{self.user.username} {self.stripe_id}'
    
    

class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.DecimalField(decimal_places=2, max_digits=6)

    def __str__(self):
        return self.code



    
    






