from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Products, Shop,Status
from datetime import date, datetime, timedelta
from django.contrib import auth
from bills.views import detailPros
# Create your views here.

@login_required(login_url='signin')
def seller(request):
    try:
        shop=request.user.userprofile.shop
    except Exception as e:
        print('Error no userProfile ')
        shop=None
    context={
        'shop':shop,
        'title':'Seller',
    }
    return render(request,'sales/seller.html',context)

@login_required(login_url='signin')
def serachPro(request):
    product=None
    shop=None
    if request.method=='POST':
        if 'inputBarcode' not in request.POST:
            messages.error(request,'do not play with us ok *_^')
            return redirect('seller')
        searchpro=request.POST['inputBarcode']
        shop=request.user.userprofile.shop

        if not shop:
            messages.error(request,'يجب التاكد من ان الموظف يتبع الى محل معين')
            return redirect('seller')
        
        if searchpro:
            
            
            if Products.objects.filter(pin=searchpro, status__name='available',shop__name=shop.name,shop__address=shop.address).exists():
                product=Products.objects.get(pin=searchpro,status__name='available',shop__name=shop.name,shop__address=shop.address)
                
                messages.success(request,f'تم الحصول على المنتج {product.name}')
                messages.info(request,f'لاتمام عملية البيع يرجى الضغط على زر (البيع) وادخال المعلومات المطلوبة')

            elif Products.objects.filter(pin=searchpro, status__name='block',shop__name=shop.name,shop__address=shop.address).exists():
                     messages.error(request,'you can not sell this product :) pls ask Admin')
                     product=Products.objects.get(pin=searchpro,status__name='block',shop__name=shop.name,shop__address=shop.address)
                    #  return redirect('seller'):
            else:
                messages.error(request,f'there is no  Product\'s Barcode {searchpro}')
                print(request.user.seller_pro.all()) ####relation_name ^_^
                return redirect('seller')
        else:
            messages.error(request,'Error you must enter Product\'s Barcode')
            return redirect('seller')
        context={
            'shop':shop,
            'pro':product,
            'title':'seller'
        }
        return render(request,'sales/seller.html',context)
    else:
        context={
                'shop':shop,
                'pro':product,
                'title':'seller'
            }
        return render(request,'sales/seller.html',context)

def remove_trailing_zeros(decimal_number):
    normalized_decimal = decimal_number.normalize()
    return str(normalized_decimal).rstrip('0').rstrip('.') if '.' in str(normalized_decimal) else str(normalized_decimal)


@login_required(login_url='signin')
def doneSell(request):

    if request.method=='POST':
        userSeller=request.user.username
        print(userSeller)
        if 'inputPrice' in request.POST and 'inputCustomer' in request.POST and 'inputid' in request.POST:
            price=request.POST.get('inputPrice')
            customer=request.POST['inputCustomer']
            id=request.POST['inputid']
            if Products.objects.filter(pk=id).exists():
                pro=Products.objects.get(pk=id)
                if pro.status.name=='block':
                    messages.error(request,'do not play with the fire ok!')
                    auth.logout(request)
                    return redirect('signin')
                pro.seller=request.user
                pro.price_sold=price
                pro.description+=f'\n name of Customer: {customer}'
                pro.sell_time=datetime.now()
                pro.status=Status.objects.get(name='sold')
                pro.save()
                messages.success(request,f'the Sell is Done by {request.user.username}')
                return redirect('seller')
        else:
            messages.error(request,'Error there is mistake ')
            return redirect('seller')
    else:
        return render(request,'sales/seller.html')    
    
@login_required(login_url='signin')
def daily_sales(request):
    shop=None
    weight24=None
    no24=None
    dict=None
    cash=0
    name_address=None
    products=None
    shops=Shop.objects.all()
    today = date.today()

    if request.method=='POST':
        if 'inputShop' in request.POST:
            name_address=request.POST['inputShop'].split('-')
            print('2121212',name_address)
            if name_address:
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    # shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    print('11111111',name_address)
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    print('55555555555555555555',shop)
                    products=Products.objects.filter(shop__name=shop.name,shop__address=shop.address,status__name='sold',sell_time__date=today)
                else:
                    messages.info(request,'في حال لم يتم اختيار فرع سيتم، عرض مبيعات كل الأفرع')
                    products=Products.objects.filter(status__name='sold',sell_time__date=today)

                weight24,no24,dict,cash=detailPros(products)

                context={
                'weight24':weight24,
                'no24':no24,
                'dict_details':dict,
                'cash':cash,

                'shops':shops,
                'shop':shop,
                'today':today,
                'daily_sales':products,
                
                'title':'Daily'
                }    
    
    
    else:
        messages.info(request,'choose one of shop')
    context={
        'weight24':weight24,
        'no24':no24,
        'dict_details':dict,
        'cash':cash,
        'shop':shop,
        'shops':shops,
        'today':today,
        'daily_sales':products,
        'title':'Daily'
    }
    return render(request,'sales/daily.html',context)

def weekly_sales(request):
    today = date.today()
    weight24=None
    no24=None
    dict=None
    start_of_week = today - timedelta(days=today.weekday())
    specific_date2 = datetime.strptime(str(start_of_week), '%Y-%m-%d')
    endDate=today + timedelta(days=1)
    print('weeeewewewew',start_of_week)
    print('weeeewewewew',today)
    print('weeeewewewew',specific_date2)
    print('weeeewewewew',endDate)

    shops=Shop.objects.all()
    shop=None
    products=None
    
    if request.method=='POST':
        if 'inputShop' in request.POST:
            name_address=request.POST['inputShop'].split('-')
            print(name_address)
            if name_address:
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    # shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    shop=Shop.objects.get(name='amoda',address='düsseldorf')
                    print(shop)
    
                    products = Products.objects.filter(shop=shop,sell_time__gte=start_of_week,status__name='sold')
                    
                    weight24,no24,dict=detailPros(products)
    context={
        
        'weight24':weight24,
        'no24':no24,
        'dict_details':dict,

        'shops':shops,
        'shop':shop,
        'today':start_of_week,
        'weekly_sales':products,
        
        'title':'Daily'
    }
    return render(request,'sales/weekly.html',context)

def monthly_sales(request):
    today = date.today()
    shop=None
    weight24=None
    no24=None
    dict=None
    cash=0

    name_address=None
    products=None
    shops=Shop.objects.all()


    if request.method=='POST':
        if 'inputShop' in request.POST:
            name_address=request.POST['inputShop'].split('-')
            
            if name_address:
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    # shop=Shop.objects.get(name='amoda',address='düsseldorf')
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    products = Products.objects.filter(shop__name=shop.name,shop__address=shop.address,sell_time__month=today.month, sell_time__year=today.year,status__name='sold')
                else:
                    messages.info(request,'في حال لم يتم اختيار فرع سيتم، عرض مبيعات كل الأفرع')
                    products=Products.objects.filter(status__name='sold',sell_time__month=today.month, sell_time__year=today.year)

                weight24,no24,dict,cash=detailPros(products)
                context={
                        'weight24':weight24,
                        'no24':no24,
                        'dict_details':dict,
                        'shop':shop,
                        'shops':shops,
                        'cash':cash,
                        
                        'month':today.month,
                        'monthly_sales':products,
                        
                        'title':'Monthly'
                }
        

    
    else:
        messages.info(request,'choose one of shop')
    context={
        'weight24':weight24,
        'no24':no24,
        'dict_details':dict,
        'shop':shop,
        'shops':shops,
        'cash':cash,
        'month':today.month,
        'monthly_sales':products,
        
        'title':'Monthly'
    }
    return render(request,'sales/monthly.html',context)

def yearly_sales(request):
    shop=None
    weight24=None
    no24=None
    dict=None
    cash=0
    name_address=''
    products=None
    today = date.today()
    shops=Shop.objects.all()

    if request.method=='POST':
        if 'inputShop' in request.POST:
            name_address=request.POST['inputShop'].split('-')
            print(name_address)
            if name_address and name_address != '---':
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    products = Products.objects.filter(shop__name=shop.name,shop__address=shop.address,sell_time__year=today.year,status__name='sold')
                else:
                    messages.info(request,'في حال لم يتم اختيار فرع سيتم، عرض مبيعات كل الأفرع')
                    products=Products.objects.filter(status__name='sold',sell_time__year=today.year)
                    
                weight24,no24,dict,cash=detailPros(products)

        context={
            'weight24':weight24,
            'no24':no24,
            'dict_details':dict,
            'cash':cash,
            'shops':shops,
            'shop':shop,
            'year':today.year,
            'yearly_sales':products,
            'title':'Yearly'
        }    
    
    
    
    else:           
        messages.info(request,'choose one of shop')
        context={

            'weight24':weight24,
            'no24':no24,
            'dict_details':dict,
            'shop':shop,
            'cash':cash,
            'shops':shops,
            'year':today.year,
            'yearly_sales':products,
            'title':'Yearly'
        } 

    return render(request,'sales/yearly.html',context)
