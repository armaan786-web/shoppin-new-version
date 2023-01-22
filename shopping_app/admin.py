from django.contrib import admin
from . models import *

# Register your models here.

admin.site.register(Profile)


@admin.register(Prodcut)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'description', 'duration', 'commission', 'product_img']


@admin.register(Recharge)
class RechargeModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'upi_id', 'amount', 'utr', 'date','recharge_request']

@admin.register(Kyc)
class RechargeModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'bank_holder_name', 'bank_name', 'account_number', 'ifsc_code']



# @admin.register(Booking)
# class BookingModelAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'product','booking_Date']


class BookAdmin(admin.ModelAdmin):
    model = Booking
    list_display = ['id', 'user', 'product','booking_Date']

    def get_name(self, obj):
        return obj.product.name
    get_name.admin_order_field  = 'product'  #Allows column order sorting
    get_name.short_description = 'Product Name'  #Renames column head

    #Filtering on side - for some reason, this works
    #list_filter = ['title', 'author__name']

admin.site.register(Booking, BookAdmin)
admin.site.register(Wallet)
admin.site.register(CouponCode)
