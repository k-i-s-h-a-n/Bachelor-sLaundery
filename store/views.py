from store.models import Product
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder


# Create your views here.
def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
    data = cartData(request)
	
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
     
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
     
    return JsonResponse('Item was added', safe=False)



def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)





from django.shortcuts import redirect
from django.shortcuts import render,HttpResponse
# from matplotlib.style import context
from datetime import datetime
from store.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login

from django.contrib.auth.forms import UserCreationForm 
from .forms import signupform





def index(request):
    return render(request,'index.html')



def services(request):
    return render(request,'services.html')


def contact(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        contact=Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
        contact.save()
        messages.success(request, 'Your response has been recorded!')
    return render(request,'contact.html')


def about(request):
    return render(request,'about.html')






from django.contrib import messages
from django.contrib import messages

from django.contrib import messages

def loginuser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.", extra_tags='danger')
            return redirect('login')

    # Clear any existing messages
    storage = messages.get_messages(request)
    storage.used = True

    return render(request, 'login.html')





from django.contrib.messages import get_messages

def signupview(request):
    if request.method == "POST":
        form = signupform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect('/login')
        else:
            if form.errors.get('password2') == ['The two password fields didn’t match.']:
                form.add_error('password2', 'Password should contain at least one uppercase letter, one special character, and one number.')
            else:
                messages.error(request, "Registration failed. Please check the form.")
    else:
        form = signupform()

    # Clear error messages when page is refreshed
    storage = get_messages(request)
    for message in storage:
        if message.level_tag == 'error':
            storage.used = True
            break

    return render(request, 'signup.html', {'form': form})







def logoutuser(request):
    logout(request)
    return redirect("/login")
