from django.urls import path
from .import views

urlpatterns = [
    path('',views.Divingpakckage1,name='Divingpakckage'),
    path('foodcat/<int:id>/',views.foodcat_view,name="foodcat"),
    path('addfood/<int:id>',views.addfood,name='addfood'),
    path('Menuform/',views.Menuview),
    path('about/',views.about,name="about"),
    path('register/',views.register,name="register"),
    path('menu/',views.menu,name="menu"),
    path('login/',views.logindetails,name="login"),
    path('logout1/',views.logout_details,name="logout1"),
    path('searchprod/',views.searchprod,name="searchprod"),
    path('addtocart/<foodid>',views.addtocart,name="addtocart"),
    path('viewtocart/',views.viewtocart,name="viewtocart"),
    path('remove_order/<int:id>',views.remove_order,name="remove_order"),
    path('updateqty/<qv>/<fid>/',views.updateqty),
    path('remove/<int:fid>',views.remove_order,name="remove_order"),
    # path('checkout1/',views.checkout1,name="checkout1"),
    path('<int:customer_id>/checkout1/',views.checkout1,name="checkout1"),
    path('range',views.range,name='range'),
    path('sort/<sv>',views.sort),    
    path('setcookie/',views.set_cookie),
    path('getcookie/',views.get_cookie),
    path('home/',views.show,name='home'),
    path('paymentfailed/',views.paymentfailed,name='paymentfailed'),
    path('paymentsuccessfull/',views.paymentsuccessfull,name='paymentsuccessfull'),
    path('adddivingpackage/<int:id>',views.adddivingpackage,name='adddivingpackage'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('details',views.detailsview,name="details"),
    # path('instructor/',views.instructor,name='instructor'),
    path('booking_ride/',views.booking_ride,name='booking_ride'),
    path('booking_ride/<int:diving_pakckage>/<int:instructor>/', views.booking_ride, name='booking_ride'),
    path('order1/',views.order_details_admin,name="order1"),
    path('order2/',views.order_details,name="order2"),
    path('drf_crud/',views.crud_view.as_view(),name='crud'),
    path('forgotpassword/',views.forgot_password, name="forgotpassword"),

    path('reset_password/<uidb64>/<token>/', views.reset_password, name='resetpassword'),

    path('password_reset_done/', views.password_reset_done, name='passwordresetdone'),
    path('product_list/', views.product_list, name='product_list'),
    path('delete/<int:id>/', views.delete_product, name='deleteprod'), 
    path('updateprod/<int:id>/',views.updateprod,name='updateprod'),
    path('update_order/<int:id>/', views.update_order, name='update_order'),
    # Delete order URL
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),


]


