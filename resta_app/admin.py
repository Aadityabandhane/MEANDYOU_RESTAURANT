from django.contrib import admin

# Register your models here.
from .models import food_category,Menu,cart,customer_details,Divingpakckage,Instructor,Booking,order

class admincategorymodel(admin.ModelAdmin):
    list_display=['food_type','image']
admin.site.register(food_category,admincategorymodel)

class Menuadmin(admin.ModelAdmin):
    list_display=['item_name','food_category','description','price','image']
admin.site.register(Menu,Menuadmin)


class cartadmin(admin.ModelAdmin):
    list_display=['uid','foodid','qty']
admin.site.register(cart,cartadmin)

class customeradmin(admin.ModelAdmin):
    list_display=['user','Name','address','city','pincode']
admin.site.register(customer_details,customeradmin)

class Divingpakckageadmin(admin.ModelAdmin):
    list_display=['Tital','description','price_per_person','image']
admin.site.register(Divingpakckage,Divingpakckageadmin)

class Instructoradmin(admin.ModelAdmin):
    list_display=['name','bio','experience_years']
admin.site.register(Instructor,Instructoradmin)

class Bookingadmin(admin.ModelAdmin):
    list_display=['user','diving_pakckage','instructor']
admin.site.register(Booking,Bookingadmin)

class orderadmin(admin.ModelAdmin):
    list_display=['customer','product','quantity','order_date','status','total_price']
admin.site.register(order,orderadmin)
