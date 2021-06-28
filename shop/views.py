from django.db.models.fields import URLField
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
import json
from .models import *


# Create your views here.

@login_required(login_url=('login'))
def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'index.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0}

    context = {'items': items, 'order': order}
    return render(request, 'cart.html', context)


def login(request):
    return render(request, 'login.html')


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0}

    context = {'items': items, 'order': order}
    return render(request, 'checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def registration(request):
    if request.POST:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        number = request.POST['number']
        address = request.POST['address']
        pass1 = request.POST['pass']
        pass2 = request.POST['re_pass']
        try:
            if Compny_Details.objects.get(email=email):

                return HttpResponse("<h1><a href=''>email alredy registered</a> </h1>")

            elif Compny_Details.objects.get(username=username):
                return HttpResponse("<h1><a href=''>username alredy registered</a> </h1>")
        except:
            if pass1 == pass2:
                obj = Compny_Details()
                obj.first_name = first_name
                obj.last_name = last_name
                obj.email = email
                obj.number = number
                obj.address = address
                obj.password = pass1  # or pass2
                obj.save()

                user = User.objects.create_user(
                    username=username, password=pass1, email=email, first_name=first_name, last_name=last_name)
                user.save()

                obj = Customer()
                obj.user = User.objects.get(email=email)
                obj.name = first_name
                obj.email = email
                obj.save()

                return redirect('login')
    return render(request, "compny/login/registration.html", {'tname': 'Registration'})


def login(request):
    if request.POST:
        username = request.POST['username']
        passd = request.POST['pass']
        print(username, passd)

        user = auth.authenticate(username=username, password=passd)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return HttpResponse("<h1><a href=''>wrong password and email</a> </h1>")

    else:
        return render(request, "compny/login/login.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):

    
    try:
        product = Compny_Details.objects.get(email=request.user.email)
        firstname = product.first_name
        lastname = product.last_name
        email = product.email
        number = product.number
        address = product.address
        
        
    except Compny_Details.DoesNotExist:
        raise Http404("Given query not found....")
       


    return render(request, "profile.html", {'tname':'Profile', 'firstname':firstname, 'lastname': lastname , 'email': email, 'number': number, 'address':address })  
    
