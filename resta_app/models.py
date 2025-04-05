from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class food_category(models.Model):
    food_type = models.CharField(max_length=100, unique=True)
    image=models.ImageField(upload_to='images/',null=True,blank=True)
    def __str__(self):
        return self.food_type
    
    
class Menu(models.Model):
    item_name=models.CharField(max_length=100)
    food_category=models.ForeignKey(food_category,on_delete=models.PROTECT)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='images/')
    
    


    def __str__(self):
        return str(self.item_name)

    

class cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    foodid=models.ForeignKey(Menu,on_delete=models.CASCADE,db_column="foodid")
    qty=models.IntegerField(default=1)
    checkout_done=models.BooleanField(default=False, null=True, blank=True)

class customer_details(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=100)
    address=models.TextField(blank=True,null=True)
    city=models.CharField(max_length=100)
    pincode=models.IntegerField(default=0,blank=True,null=True)

# class feedback(models.Model):
#     cid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
#     feedback=models.TextField(blank=True,null=True)
#     rating=models.

class Divingpakckage(models.Model):
    Tital=models.CharField(max_length=255)
    description=models.TextField()
    price_per_person=models.DecimalField(max_digits=10,decimal_places=2)
    image=models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.Tital


class Instructor(models.Model):
    name=models.CharField(max_length=255)
    bio=models.TextField()
    experience_years=models.IntegerField()
    
    def __str__(self):
        return self.name
    
    
class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    diving_pakckage=models.ForeignKey(Divingpakckage,on_delete=models.CASCADE)
    instructor=models.ForeignKey(Instructor,on_delete=models.CASCADE)
    
    
class order(models.Model):
    STATUS_CHOICES=[
        ('PENDEING','pending'),
        ('PROCESSING','processing'),
        ('SHIPPED','shipped'),
        ('DELIVERED','delivered'),
        ('CANCELLED','cancelled')
    ]
    
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    product=models.ForeignKey(Menu,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    order_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='PENDEING')
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
   
    def __str__(self):
        return f"order #{self.id} - {self.status}"
