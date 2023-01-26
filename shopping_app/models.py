from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from .utils import generate_ref_code
import math
from django.db.models import Sum

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(to=User,on_delete=CASCADE)
    mobile = models.CharField(max_length=100)
    referral_id = models.CharField(max_length=12,blank=True)
    refer_by = models.CharField(max_length=50,null=True,blank=True)

    
    def save(self, *args, **kwargs):
        if self.referral_id == "":
            user_id = (generate_ref_code())
            self.referral_id = user_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.first_name
    

    # def __str__(self):
    #     return self.user.username




class Prodcut(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    duration = models.IntegerField()
    commission = models.IntegerField()
    product_img = models.ImageField(upload_to="product_img")

    def __str__(self):
        return self.name
    


recharge_request = (
    ("Pending","Pending"),
    ("Accept","Accept"),
    ("Reject","Reject"),
    
) 

class Recharge(models.Model):
    user = models.ForeignKey(to=Profile,on_delete=CASCADE)
    upi_id = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    utr = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    remaining_amount = models.PositiveIntegerField(default=0)
    total_amount = models.PositiveIntegerField(default=0)
    recharge_request = models.CharField(max_length=50,choices=recharge_request,default="Pending")

    @property
    def total_cost(self):
        user_recharge = Recharge.objects.filter(user=self.user,recharge_request="Accept")
        total_amount= sum(booking.amount for booking in user_recharge)   
        # total_amount = total_amount-self.remaining_amount
    
        return total_amount

    @property
    def remaing_amt(self):
        
        return self.remaing_amt-self.remaining_amount
        
        
        # return self.total_cost-self.remaining_amount
        
    
       
class Booking(models.Model):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    product = models.ForeignKey(Prodcut,on_delete=models.CASCADE)
    booking_Date = models.DateField(auto_now_add=True)
    daily_wise_commission = models.IntegerField(default=0,null=True,blank=True)   
    
    def __str__(self):
        return self.user.user.username


    @property
    def total_purchase(self):
        totalpurchase = Booking.objects.filter(user=self.user)
        total_amount= sum(booking.product.price for booking in totalpurchase)   
        return total_amount
        
    # def update_user_total_commission(self):
    #     user_bookings = Booking.objects.filter(product=self.product)
    #     total_commission = sum(booking.daily_wise_commission for booking in user_bookings)
       
    #     return total_commission
    
   

    
    

class Kyc(models.Model):
    user = models.ForeignKey(to=Profile,on_delete=CASCADE)
    bank_holder_name=models.CharField(max_length=50)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=50)

    def __str__(self):
        return self.user



class commision(models.Model):
    booking = models.ForeignKey(to=Booking,on_delete=CASCADE)
    commision = models.IntegerField()

    def __str__(self):
        return self.booking.user
    

    

wallet_request = (
    ("Pending","Pending"),
    ("Accept","Accept"),
    ("Reject","Reject"),
    
) 
class Wallet(models.Model):
    
    user = models.ForeignKey(to=Booking,on_delete=CASCADE)
    amount = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    wallet_request = models.CharField(max_length=50,choices=wallet_request,default="Pending")


coupen_request = (
    ("Pending","Pending"),
    ("Accept","Accept"),
    ("Reject","Reject"),
    
) 

class CouponCode(models.Model):
    user = models.ForeignKey(to=Profile,on_delete=CASCADE)
    coupon_code = models.CharField(max_length=50) 
    gift_amt = models.IntegerField(default=0,null=True,blank=True)   
    coupen_request = models.CharField(max_length=50,choices=coupen_request,default="Pending")
    date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now_add=False, auto_now=True, null=True)

    @property
    def total_gift(self):
        user_gift = CouponCode.objects.filter(user=self.user,coupen_request="Accept")
        total_gift= sum(coupon.gift_amt for coupon in user_gift)   
        # total_amount = total_amount-self.remaining_amount
    
        return total_gift

    def __str__(self):
        return self.user.user.first_name
    

withdraw_request = (
    ("Pending","Pending"),
    ("Accept","Accept"),
    ("Reject","Reject"),
    
) 
class Withdraw(models.Model):
    user = models.ForeignKey(to=Profile,on_delete=CASCADE)
    amount = models.IntegerField(default=0)
    withdraw_request = models.CharField(max_length=50,choices=withdraw_request,default="Pending")
    date = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now_add=False, auto_now=True, null=True)
    def __str__(self):
        return self.user.user.first_name
    
