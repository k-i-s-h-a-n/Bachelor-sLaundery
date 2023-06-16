from django.urls import path
from . import views

urlpatterns = [
    path('services/add services/', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    
    
    
    
    path('login/',views.loginuser,name="login"),
    path('logout',views.logoutuser,name="logout"),
    path('signup',views.signupview,name="signup"),
    path('',views.index,name='home'),
    path('services/',views.services,name='services'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
]