from datetime import date
from django.shortcuts import render,redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from pages.views import detailPros

# Create your views here.
def signin(request):

    context={
        'title':'Signin',
    }
    print('btnanmeldung' in request.POST)
    print(request.method=='POST')
    
    if request.method=='POST' and 'btnanmeldung' in request.POST:
        username=request.POST['username']
        print('username',username)
        password=request.POST['pass']
        print('ok')
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request,user)
        else:
            messages.error(request,'Username or PassWord Invald')
            print('Error')
        if username !='admin' and not request.user.is_anonymous:
            username=request.user.username
            try:
                shop=request.user.userprofile.shop
                messages.success(request,f'welcome {username} you are employee in {shop.name} {shop.address}')
                return redirect('seller')
            except Exception as e:
                print('Error')
                
                messages.error(request,f'You must connect with Admin to add profile for you')
                return redirect('signin')
        
        return redirect('dashboard')
    else:
        return render(request,'accounts/signin.html',context)

def signup(request):
    context={
        'title':'SignUp'
    }
    return render(request,'accounts/signup.html',context)

@login_required(login_url='signin')
def profile(request):

    if request.user.is_authenticated and not request.user.is_anonymous:
        weight24=None
        no24=None
        dict=None
        cash=0
        shop=None
        today = date.today()
        user=request.user
        products=user.seller_pro.filter(status__name='sold').order_by('-sell_time')[0:5]
        products_No=user.seller_pro.all().count()
        monthly_sales = user.seller_pro.filter(sell_time__month=today.month, sell_time__year=today.year,status__name='sold')
        monthly_sales_NO = user.seller_pro.filter(sell_time__month=today.month, sell_time__year=today.year,status__name='sold').count()
        print(products.count())

        weight24,no24,dict,cash=detailPros(monthly_sales)
        try:
            shop=user.userprofile.shop
        except Exception as e:
            print('Error in accout view')
            messages.error(request,'you masst make profile connect with Admin')
        context={
            'weight24':weight24,
            'no24':no24,
            'dict_details':dict,
            'cash':cash,
            'shop':shop,
            'products':products,
            'products_no':products_No,

            'monthly_sales':monthly_sales,
            'monthly_sales_no':monthly_sales_NO,
            'title':'profile'
        }

        return render(request,'accounts/profile.html',context)
    else:
        messages.error(request,'you must log in')
        return redirect('signin')

@login_required(login_url='signin')
def profile_staff(request,staff_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        if User.objects.filter(pk=staff_id).exists():
          user=User.objects.get(pk=staff_id)

        today = date.today()

        products=user.seller_pro.filter(status__name='sold').order_by('-sell_time')[0:5]
        products_No=user.seller_pro.all().count()
        monthly_sales = user.seller_pro.filter(sell_time__month=today.month, sell_time__year=today.year,status__name='sold')
        monthly_sales_NO = user.seller_pro.filter(sell_time__month=today.month, sell_time__year=today.year,status__name='sold').count()
        print(products.count())
        context={
            'products':products,
            'products_no':products_No,
            'user':user,
            'monthly_sales':monthly_sales,
            'monthly_sales_no':monthly_sales_NO,
            'title':'profile',
        }
        return render(request,'accounts/profile_staff.html',context)
    else:
        messages.error(request,'you must log in')
        return redirect('signin')


def logout(request):

    if request.user.is_authenticated and not request.user.is_anonymous:
        auth.logout(request)
        messages.success(request,'logout is done')
    return redirect('signin')

def newUser(request):
    context={
        'title':'SignUp'
    }
    return render(request,'accounts/newUser.html',context)