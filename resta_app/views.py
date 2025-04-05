from django.shortcuts import render,HttpResponse,redirect
from .models import food_category,Menu,User,cart,Divingpakckage,order,customer_details,Instructor,Booking
from .forms import Menuform,registrationform,menu_detailsform,userauthenticationForm,Customerform
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# rest_framework**********
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import customerserializer
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.views import View
# Create your views here.
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
import uuid
from django.conf import settings

User = get_user_model()

def show(request):
    category=food_category.objects.all()
    menu=Menu.objects.all()
    context={}
    context['food_category']=category
    context['menu']=menu
    return render(request,'resta.html',context)

def foodcat_view(request,id):
    category=food_category.objects.all()
    menu=Menu.objects.filter(food_category=id)
    context={}
    context['food_category']=category
    context['menu']=menu
    return render(request,'resta.html',context)

def addfood(request,id):
    product=Menu.objects.filter(id=id)
    context={}
    context['product']=product
    category=product[0].food_category
    menu=Menu.objects.filter(food_category=category).exclude(id=id) 
    context['menu']=menu
    context['menu']=menu
    return render(request,'product.html',context)



def Menuview(request):
    if request.method=="POST":
        FM=Menuform(request.POST)
        if FM.is_valid():
            return redirect('resta')
    else:
        FM=Menuform()
        return render(request,"Menuform.html",{"FM":FM})
    

def register(request):
    if request.method == "POST":
        RF = registrationform(request.POST)
        if RF.is_valid():
            print('here', RF.cleaned_data)
            
           
            if RF.cleaned_data['first_name'].isalpha() and RF.cleaned_data['last_name'].isalpha():
                email=RF.cleaned_data['email']

                users = User.objects.filter(email=email)

                if users.exists():
                    return render(request, "register.html", {'RF': RF, 'error': "Email already exists"})

                RF.save()
                return redirect('login')  
            return render(request, "register.html", {'RF': RF, 'error': "First and Last names should contain only alphabets."})
        
       
        return render(request, "register.html", {"RF":RF})
    
    else:
       
        RF = registrationform()
        return render(request, "register.html",{"RF":RF})




# def register(request):
#     if request.method=="POST":
#         RF=registrationform(request.POST)
#         if RF.is_valid():
#             RF.save()
#             return redirect('home')
#         else:
#             RF=registrationform()
#             return render(request,"register.html",{"RF":RF,'msg':'Worong credentials...!'})
#     else:
#         RF=registrationform()
#         return render(request,"register.html",{"RF":RF})
    
from django.shortcuts import render, redirect
from .forms import menu_detailsform 

def menu(request):
    if request.method == "POST":
        MF = menu_detailsform(request.POST, request.FILES)
        if MF.is_valid():
            MF.save()
            return redirect('home') 
        else:
            return render(request, "menu.html", {"MF": MF})
    else:
        MF = menu_detailsform()
    
    return render(request, "menu.html", {"MF": MF})  # Ensure response is always returned


import datetime
def logindetails(request):
    if request.method=="POST":
        uname=request.POST["username"]
        upass=request.POST["password"]
        user=authenticate(request,username=uname,password=upass)
        
        if user is not None:
            login(request,user)
            response=redirect('home')
            request.session['username']=uname
            response.set_cookie('username',uname)
            response.set_cookie('time',datetime.datetime.now())
            return response
        else:
            LDF=userauthenticationForm()
            return render(request,"login.html",{"LDF":LDF,'msg':'Worong password or username...!'})
    else:
        LDF=userauthenticationForm()
        return render(request,"login.html",{"LDF":LDF})
    
def logout_details(request):
    logout(request)
    return redirect('home')

def searchprod(request):
    if request.method=='POST':
        data=request.POST['search']
        searchfood=Menu.objects.filter(item_name__icontains=data)
        return render(request,'search.html',{'searchfood':searchfood})
    else:
        return redirect('home')


from django.db.models import Q
@login_required(login_url='login')
def addtocart(request,foodid):
    if request.user.is_authenticated:        
        userid=request.user.id 
        u=User.objects.filter(id=userid)
        f=Menu.objects.filter(id=foodid)
        
        c=cart.objects.filter(Q(uid=u[0]) & Q(foodid=f[0]))
        n=len(c)
        context={}
        context['product']=f
        if n==1:
            context['msg']='You have already odered..!'
            return render(request,'product.html',context)
        else:
             c=cart.objects.create(uid=u[0],foodid=f[0])
             c.save()
             context['success']='oreder added successfully...!'
             return render(request,'product.html',context)
            
    
def viewtocart(request):
    userid=request.user.id
    data=cart.objects.filter(uid=userid)
    total=0
    for x in data:
        total=total+x.foodid.price*x.qty
    context={}
    context['data']=data
    context['total']=total
    # product=Menu.objects.filter(id=foodid)
    # context={}
    # context['product']=product
    return render(request,'viewtocart.html',context)
   
def remove_order(request,id):
    c=cart.objects.filter(id=id)
    c.delete()
    return redirect('viewtocart')

def updateqty(request,qv,fid):
    cart_data=cart.objects.filter(id=fid)
    if qv=='1':
        total_qty=cart_data[0].qty+1
        cart_data.update(qty=total_qty)
    else:
        if cart_data[0].qty>1:
            total_qty=cart_data[0].qty-1
            cart_data.update(qty=total_qty)
        pass
    return redirect('/viewtocart')
    
def remove_order(request,fid):
    cart_data=cart.objects.filter(id=fid)
    cart_data.delete()
    return redirect('/viewtocart')
    
def checkout1(request, customer_id):
    userid=request.user
    # data=cart.objects.filter(uid=userid, checkout_done=False)
    data=cart.objects.filter(uid=userid)
    total=0
    delivary_charges=70
    total=0
    for x in data:
        total=total+x.foodid.price*x.qty
    final_price=delivary_charges + total
    context={}
    context['data']=data
    context['delivary_charges']=delivary_charges
    context['total']=total
    
    
    if request.method=="POST":
        fm=Customerform(request.POST)
        if fm.is_valid():
            task=fm.save(commit=False)
            task.user=request.user
            task.save()
            return redirect('details')
            
        else:
            RF=registrationform()
            return render(request,"checkout1.html",{"forms":fm,'msg':'Worong credentials...!'})
        
    fm=Customerform()
    print(fm)
    context['forms']=fm
    
    customer=customer_details.objects.filter(id=customer_id, user=request.user)
    
    
    host=request.get_host()

    paypal_checkout={
        'business':settings.PAYPAL_RECEIVER_EMAIL,
        'amount':final_price,
        'item_name':'Menu',
        'invoice':uuid.uuid4(),
        'currency_code':'USD',
        'notify_url':f"http://{host}{reverse('paypal-ipn')}",
        'return_url':f"http://{host}{reverse('paymentsuccessfull')}",
        'cancel_url':f"http://{host}{reverse('paymentfailed')}",
    }
    
    paypal_payment=PayPalPaymentsForm(initial=paypal_checkout)
    
    context['paypal']=paypal_payment
    context['final_price']=final_price
    context['item_name']=data
    context['total']=total
    context['customer_details']=customer
    return render(request,'checkout1.html',context)
   
def paymentfailed(request):
    pass

def paymentsuccessfull(request):
    userid=request.user.id
    orders=cart.objects.filter(uid=userid)
    total=0
    for i in orders:
        total_data=total+i.foodid.price*i.qty
        conform_orders=order.objects.create(product=i.foodid,customer=i.uid,quantity=i.qty,total_price=total_data)
        conform_orders.save()
        i.delete()
    fixorders=order.objects.filter(customer=request.user.id)
    context={}
    context['fixorder']=fixorders
    return render(request,'paymentsuccessfull.html',context)

   

def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__lte=max) #5000
    q2=Q(price__gte=min) #1000
    c=cart.objects.filter(q1 & q2)# select * from pet where
    context={}
    context['menu']=c
    return render(request,'index.html',context)

def sort(request,sv):
    if sv=='0':
        col='price' #asc
    else:
        col='-price' #desc
    menu=cart.objects.all().order_by(col) #select * from product
    context={}
    context['menu'] =menu
    return render(request,'resta.html',context)

def about(request):
    return render(request,'about.html')


def set_cookie(request):
    response=HttpResponse("cookie has been set!!")
    response.set_cookie('username','aditya')
    return response

def get_cookie(request):
    username=request.COOKIES.get('username')
    return render(request,'getcookie.html',{'username':username})


def Divingpakckage1(request):
    packages=Divingpakckage.objects.all()
    context={}
    context['packeges']=packages
    return render(request,'index.html',context)

def adddivingpackage(request,id):
    Divingpack=Divingpakckage.objects.filter(id=id)
    context={}
    context['Divingpack']=Divingpack
    return render(request,'adddivingpackage.html',context)

def placeorder(request):
    userid=request.user.id
    orders=cart.objects.filter(uid=userid)
    total=0
    for i in orders:
        total_data=total+i.foodid.price*i.qty
        conform_orders=order.objects.create(product=i.foodid,customer=i.uid,quantity=i.qty,total_price=total_data)
        conform_orders.save()
    fixorders=order.objects.filter(customer=request.user.id)
    context={}
    context['alldata']=fixorders
    return render(request,'placeorder.html',context)
        

def detailsview(request):
    userid=request.user
    data=cart.objects.filter(uid=userid)
    total=0
    delivary_charges=70
    total=0
    for x in data:
        total=total+x.foodid.price*x.qty
    final_price=delivary_charges + total
    context={}
    context['data']=data
    context['delivery_charges']=delivary_charges
    context['total']=total
    context['finalprice']=final_price
    
    if request.method=="POST":
        fm=Customerform(request.POST)
        if fm.is_valid():
            task=fm.save(commit=False)
            task.user=request.user
            task.save()
            print(task.id, task.Name)
            return redirect(reverse('checkout1', args=[task.id]))
            
        else:
            RF=registrationform()
            return render(request,"details.html",{"forms":fm,'msg':'Worong credentials...!'})
        
    fm=Customerform()
    context['forms']=fm
    
    customer=customer_details.objects.filter(user=request.user)

    context['final_price']=final_price
    context['item_name']=data
    context['total']=total
    context['customer_details']=customer
    return render(request,'details.html',context)

'''
def instructor(request):
    Instructorinfo=Instructor.objects.all()
    context={}
    context['Instructorinfo']=Instructorinfo
    return render(request,'instructor.html',context)

'''

# def instructor(request):
#     Instructorinfo = Instructor.objects.all() 
#     context={}                                       # Fetch all instructors
#     context ['Instructorinfo'] = Instructorinfo  # Pass them to the template

   
#     # if not Instructorinfo.exists():
#     #     context['message'] = "No instructors available."

#     return render(request, 'instructor.html', context)


def order_details(request):
    orders=order.objects.filter(customer=request.user)
    return render(request,'order1.html',{'orders':orders})


def order_details_admin(request):
    orders=order.objects.all()
    return render(request,'order1.html',{'orders':orders})




@login_required(login_url='login')
def booking_ride(request,diving_pakckage,instructor):
    if request.user.is_authenticated:
       userid=request.user.id
       u=User.objects.filter(id=userid)
       p=Divingpakckage.objects.filter(id=diving_pakckage)
       ins=Instructor.objects.filter(id=instructor)
       q1=Q(uid=u[0])
       b=Booking.objects.filter(Q(uid=u[0]) & Q(id=p[0]) & Q(id=ins[0]))
       n=len(b)
       context={}
       context={'data':p}
       if n==1:
           context['msg']='ride is already in  booking list'
           return render(request,'booking_ride.html',context)
       else:
           b=Booking.objects.create(uid=u[0],did=p[0])
           b.save()
           context['success']='ride added successfully to book'
           return render(request,"booking_ride.html",context)


class crud_view(APIView):
    def post(self,request):
        customer_data = request.data
        print(customer_data)
        serializer=customerserializer(data=customer_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Success":"Data is successfully saved"}, status=status.HTTP_200_OK)
        
    def get(self,request):
        id = request.data.get('id',None)
        if id:
            try:
                data=customer_data.objects.get(id=id)
                serializer=customerserializer(data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except:
                return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        else:
            customer_data=customer_details.objects.all()
            serializer = customerserializer(customer_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self,request):
        update_data = request.data
        id = request.data.get('id',None)
        if id:
           customer_data=customer_details.objects.get(id=id)
           serializer=customerserializer(customer_data,update_data,partial=True)
           if serializer.is_valid():
               serializer.save()
               return Response({"Success":"Data is successfully Updated"}, status=status.HTTP_200_OK)
               


    def delete(self,request):
        id = request.data.get('id',None)
        customer_data=customer_details.objects.get(id=id)
        if id:
            customer_data.delete()
            return Response({"Success":"Data is successfully deleted"}, status=status.HTTP_200_OK)
        

def forgot_password(request):          

    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(f'/reset_password/{uidb64}/{token}/')           
            send_mail(
                'Password Reset',
                f'Click the given link to reset your password: {reset_url}',
                settings.EMAIL_HOST_USER,  # Use a verified email address
                [email],
                fail_silently=False,
            )
            return redirect('passwordresetdone')
        else:
            print('I am executed')
           
    print('I am executed')
    return render(request,'forgot_password.html')


def reset_password(request, uidb64, token):
    if request.method == 'POST':
        password = request.POST['password']
        print(password)
        password2 = request.POST['password2']
        print(password2)
        if password == password2:
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
                if default_token_generator.check_token(user, token):
                    user.set_password(password)
                    user.save()
                    return redirect('login')
                else:
                    return HttpResponse('Token is invalid', status=400)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return HttpResponse('Invalid link', status=400)
        else:
            return HttpResponse('Passwords do not match', status=400)
    return render(request, 'reset_password.html')

def password_reset_done(request):
    return render(request, 'password_reset_done.html')


def product_list(request):
    products = Menu.objects.all() 
    return render(request, 'productlist.html', {'products': products})


def delete_product(request, id):
    deleteMenu=Menu.objects.filter(id=id)
    deleteMenu.delete()
    return redirect('product_list')

     

def updateprod(request, id):

    product = Menu.objects.get(id=id)
    
    if request.method == "POST":
        FM = menu_detailsform(request.POST,request.FILES,instance=product)  
        if FM.is_valid():
            FM.save()  
            return redirect('product_list')
        else:
            return render(request, "update.html", {"FM": FM, "errors": FM.errors})  
    else:
        FM = menu_detailsform(instance=product) 
        return render(request, "update.html", {"FM": FM})
 
from django.shortcuts import get_object_or_404, render, redirect
from .models import order as order_model 


def update_order(request,id):
    order = get_object_or_404(order_model, id=id)
    
    if request.method == 'POST':
        order.status = request.POST.get('status') 
        order.save()  
        return redirect('order1') 
    return render(request, 'order1.html',{'status':status})


def delete_order(request, id):
    order = get_object_or_404(order_model, id=id)
    
    if request.method == 'POST':
        order.delete() 
        return redirect('order1')

    # Optional: Render a confirmation page before deletion
    return render(request, 'delete_confirmation.html', {'order':order})