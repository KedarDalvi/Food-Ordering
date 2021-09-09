from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import detail,MenuItem,Category,Order
import re
import string
from django.urls import reverse
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from collections import Counter 
from datetime import datetime,timedelta
from django.http import JsonResponse
import json
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings
import razorpay



email_regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'


def Email_validation(request):
    if request.method=="GET":
        try:
            user = User.objects.get(username=request.GET.get('name'))
            if re.search(email_regex, request.GET.get('name')) == None:
                wrong = True
                data = {'wrong': wrong}
            else:
                correct = True
                data = {'correct_but_used': correct}
        except User.DoesNotExist:
            if re.search(email_regex, request.GET.get('name')) == None:
                wrong = True
                data = {'wrong': wrong}
            else:
                data = {'available': True}
        return JsonResponse(data)

def home(request):
    if request.method=="GET":
        cart = request.session.get('cart')#accessing the session cart
        if request.user.is_authenticated:  
                user_id=request.session.get("user_id")
                user = User.objects.get(pk=user_id)
                x = datetime.now()#it will generate the date time at this moment
                if user.last_login >= x-timedelta(seconds=4):#we are checking that user's last_login time
                    profile =  detail.objects.get(user=request.user)
                    if profile.first_login == False:#if user is logging in first time he's dict_item is none so 
                        #we are assigning a empty dictionary to it
                        request.session['cart'] = {}
                    if profile.dict_item is not None:
                        lst=list(profile.dict_item.split(" "))
                    else:
                        lst=[]
                    for i in lst:
                        if i == '' or i== '0':
                            lst.remove(i)
                    d=Counter(lst)#we are using counter for counting which list item is appered how many times and made a dictionary
                    dict1=dict(d)
                    request.session['cart'] = dict1
        appetizers=MenuItem.objects.filter(category__name__contains="Appetizer")#created a list based on category
        fast_food=MenuItem.objects.filter(category__name__contains="fast_food")
        beverages=MenuItem.objects.filter(category__name__contains="Beverage")
        desserts=MenuItem.objects.filter(category__name__contains="Dessert")
        pizzas = MenuItem.objects.filter(category__name__contains="Pizza")
        burgers = MenuItem.objects.filter(category__name__contains="Burger")

        context= {
            'appetizers':appetizers,
            'fast_food':fast_food,
            'beverages':beverages,
            'desserts':desserts,
            'pizzas':pizzas,
            'burgers':burgers
        }

        return render(request,'main/home.html',context )
    else:
        return home_post(request)


def home_post(request):
    if request.user.is_anonymous:
            return redirect('main-signin')
    if request.method=="POST":
        request.session['last_visited_page']='home'
        return item_add_sub(request)
            

def register(request):
    if request.method=="POST":
        data=request.POST
        first_name=data['firstname']
        last_name=data['lastname']
        phone_no=data['phone_no']
        email=data['email']
        address=data['address']
        password1=data['password1']
        password2=data['password2']
        if (first_name.isalpha()==False or last_name.isalpha()==False):
            #messages.info(request,"Enter valid Name!")
            return render(request,'main/register.html',{'message1':"Enter valid Name!",'wrong_credentials':1})
        if re.search(email_regex, email) == None:
            #messages.info(request,'Enter a valid email id.')
            return render(request, 'main/register.html',{'message1':'Enter a valid email id.','wrong_credentials':1})
        if (int(phone_no[0])<=6):
            #messages.info(request,"Enter a valid phone No!")
            return render(request,'main/register.html',{'message1':"Enter a valid phone No!",'wrong_credentials':1})
        if(password1==password2):
            try: 
                user=User.objects.get(email=email) 
                #messages.info(request,"User Already Exists!")
                return render(request,'main/register.html',{'message1':"User Already Exists!",'wrong_credentials':1})
            except User.DoesNotExist:
                user=User.objects.create_user(username=data['email'],first_name=first_name,last_name=last_name,email=email,password=password1)
                user.save()
                #dict_item = {}
                profile=detail(user=user,phone_no=int(phone_no),address=address)
                profile.save()
                request.session['user_id'] = user.id
                request.session['user_phone_no']= profile.phone_no
                request.session['email'] = user.email
                request.session['name']= user.first_name+" "+user.last_name
                #messages.info(request,"User Created Sucessfully!")
                return Email_sender(request)
        #messages.info(request,"Passwords didn't Match!")
        return render(request,'main/register.html',{'message1':"Passwords didn't Match!",'wrong_credentials':1})
    return render(request,'main/register.html')


def signin(request):
    if request.method=="GET":
        return render(request,'main/signin.html')
    else:
        data=request.POST
        username=data['email']
        email=data['email']
        password=data['password']
        user=auth.authenticate(username=username,email=email, password=password)
        profile =detail(user=user)
        if user is not None:
            auth.login(request,user)
            request.session['user_id'] = user.id
            request.session['user_phone_no']= profile.phone_no
            request.session['name']= user.first_name+" "+user.last_name
            request.session['user_email']= user.email
            return redirect("main-home")
        else:
            return render(request,'main/signin.html',{'message':'Wrong Credentials!','wrong_credential':1})
           
   
@login_required(login_url="main-signin")   
def logout(request):
    if request.method=="GET":
        user_id=request.session.get("user_id")
        user = User.objects.get(pk=user_id)
        profile =  detail.objects.get(user=request.user)
        profile.first_login=True 
        profile.save(update_fields=['first_login'])
        auth.logout(request)
        messages.info(request,"User logged out!")
        return redirect('main-home')


@login_required(login_url="main-signin")
def cart(request):
    if  request.session.get('cart')=={} :
                return render(request,'main/empty_cart.html')
    if request.method=="GET":
        if request.user.is_authenticated:
            ids=list(request.session['cart'].keys())
            items = MenuItem.itmes_by_id(ids)
            context={
                'items':items
            }
            return render(request,'main/cart.html',context)
        else:
            return render(request,'main/cart.html',{'message':"You need to login first!"})
    if request.method=="POST":
        request.session['last_visited_page']="cart"
        return item_add_sub(request)


def Team(request):
    if request.method=="GET":
        return render(request,'main/Web_team.html')


def item_add_sub(request):
    item=request.POST.get('item')
    remove=request.POST.get('remove')
    delete=request.POST.get('delete')
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(item)
        if quantity:
            if delete:
                cart.pop(item)
            elif remove:
                if quantity<=1:
                    cart.pop(item)
                else:
                    cart[item] = quantity - 1
            elif item:
                cart[item] = quantity + 1
            else:
                pass
        else:
            cart[item] = 1
    else:
        cart = {}
        cart[item] = 1
    user_id=request.session.get("user_id")
    user = User.objects.get(pk=user_id)
    profile =  detail.objects.get(user=request.user)
    request.session['cart'] = cart
    if profile.dict_item is not None:
        dict_item = profile.dict_item.split(" ")
    else:
        dict_item =[]
    if remove:
        dict_item.remove(item)
    elif delete:
        dict_item = [x for x in dict_item if x != item]
    else:
        dict_item.append(item)
    profile.dict_item = " ".join(map(str, dict_item))
    profile.save(update_fields=['dict_item'])
    if request.session.get("last_visited_page")=='home':
        return redirect('main-home')
    if request.session.get("last_visited_page")=='search':
        request.session['from_item_add_sub'] = 1
        return redirect('search')
    return redirect('main-cart')


@login_required(login_url="main-signin")   
def checkout(request):
    if request.method =="POST":
        amount = 50000
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11' # OPTIONALclient.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)
        client =razorpay.Client(auth=('rzp_test_JTA0Jn9e0K4hY4', 'cO6lsSuCZ317JOX5YvIwe4B7'))
        payment = client.order.create({'amount':amount,'order_currency':'INR','payment_capture':'1'})
    return redirect('main-cart')


@csrf_exempt
def success(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    profile = detail.objects.get(user = user)
    full_name = user.first_name +" "+ user.last_name
    phone_no = profile.phone_no
    email = user.email
    username = user.email
    address = profile.address
    cart = request.session.get('cart')
    item_list=list(cart.keys())
    items = MenuItem.itmes_by_id(item_list)
    for item in items:
        order=Order(username=username, 
                        item_name=item.name,  
                        item=item,
                        item_description =item.description,
                        user = profile,
                        name=full_name,
                        email=email,
                        address=address,
                        phone_no=phone_no,
                        quantity=cart.get(str(item.id)),
                        price = item.price
                        )
        order.save()
    request.session['cart']= {}
    profile.dict_item= 0
    profile.save(update_fields=['dict_item'])
    return render(request, "main/success.html")


@login_required(login_url="main-signin")
def my_profile(request):
    if request.method =='GET':
        user_id=request.session.get("user_id")
        user= User.objects.get(pk=user_id)
        profile= detail.objects.get(user =user )
        first_name = user.first_name 
        last_name = user.last_name
        phone_no = profile.phone_no
        email = user.email
        address = profile.address
        orders = Order.get_orders_by_user(profile=profile)
        context ={
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'phone_no':phone_no,
            'address': address,
            'orders':orders
            }
        return render(request,'main/profile.html',context)



def Email_sender(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(pk=user_id)
    name = user.first_name +" " + user.last_name
    subject = 'Thanks for signing up with OFO!'
    message = render_to_string('main/email_template.html',{'name':name })
    recipient = user.email
    send_mail(subject, 
        message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    return render(request,'main/register.html',{'message_success':"User Created Sucessfully!",'wrong_credentials':1})


def error404(request, exception):
    return render(request,'main/error.html')

def search(request):
    if request.method =="GET":
        search = request.GET.get('search_dish')
        if request.session.get('from_item_add_sub') == 1:
            search = request.session.get("search")
            print("hello")
        elif search is None:
            print('search_none')
            request.session['from_item_add_sub'] = 0
            return  search_post(request)
        search = search.lower()
        final_search = search.translate({ord(c): None for c in string.whitespace})
        request.session['search'] = search 
        if final_search == "pizza":
            dishes1 = MenuItem.objects.all().filter(category__name__contains="Pizza")
        elif final_search == "appetizer" :
            dishes1 = MenuItem.objects.all().filter(category__name__contains="Appetizer")
        elif final_search == "desserts" :
            dishes1 = MenuItem.objects.all().filter(category__name__contains="Dessert")
        elif final_search == "beverage":
            dishes1 = MenuItem.objects.all().filter(category__name__contains="Beverages")
        elif final_search == "burger":
            dishes1 = MenuItem.objects.all().filter(category__name__contains="Burger")
        else:
            dishes1 = []
            dishes = MenuItem.objects.all()
            print(final_search)
            for dish in dishes:
                dish_name = dish.name.lower()
                final_dish_to_search = dish_name.translate({ord(c): None for c in string.whitespace})
                print(final_dish_to_search)
                if final_dish_to_search == final_search:
                    dishes1.append(dish)
            print(dishes1)
        context = {"dishes":dishes1}
        request.session['from_item_add_sub'] = 0
        return render(request,'main/search.html',context)
    else:
        return  search_post(request)

def search_post(request):
    if request.user.is_anonymous:
            return redirect('main-signin')
    request.session['last_visited_page']='search'
    return item_add_sub(request)
            