from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from products.models import Shop,Classes,Products
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
# Create your views here.
from .decorators import handle_database_error

def dashboard(request):

    shop=None
    weight_percentage=0
    unit_sold=''
    unit_available=''
    unit=''
    total_weight_ava=0
    total_weight_sold=0
    total_money_sold=0
    sum_gold_available=0
    pro_available=None
    sum_gold_sold=0
    shop=None

    today = date.today()
    yesterday = datetime.now() - timedelta(days=1)
    all_shops =Shop.objects.all().order_by('startWork')
    shops_info = [] #list

    shops_info=main_shops()

    classes=Classes.objects.all()
    if classes:
        for cl in classes:
            if Products.objects.filter(classes__name=cl.name,status__name='available').exists():
                pro_available=Products.objects.filter(classes__name=cl.name,status__name='available')
                # print('cl:',cl.name)
                # print('pro_available:',pro_available)
                sum_gold_available+=pro_available.count()
                if cl.name=='24':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp =total_weight_ava_temp['total_weight_ava']*1
                    total_weight_ava+= total_weight_ava_temp* 1

                    # print('total_weight_ava$$$',total_weight_ava)
                elif cl.name=='22':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.916)
                elif cl.name=='21':
                    # print('cl:',cl.name)
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.975)
                    print('total_weight_ava____21',total_weight_ava)
                elif cl.name=='18':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.875)
                elif cl.name=='14':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp*Decimal(0.585)
                elif cl.name=='8':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp*Decimal(0.333)
                else:
                    total_weight_ava = pro_available.aggregate(total_weight_ava=Sum('weight'))
        print(total_weight_ava)
        # total_weight_ava=total_weight_ava['total_weight_ava']

        if total_weight_ava:
            if total_weight_ava>1000:
                total_weight_ava=round(total_weight_ava/1000,5)
                unit_available='KG'
            else:
                total_weight_ava=round(total_weight_ava,4)
                unit_available='G'
    else:
        messages.warning(request,'there is No (AVAILABLE) Items & (Classes)')
        pro_available=None

    if Products.objects.filter(status__name='sold').exists():
        pro_sold=Products.objects.filter(status__name='sold')

        sum_gold_sold=pro_sold.count()
        total_weight_sold= pro_sold.aggregate(total_weight_sold=Sum('weight'))
        total_money_sold = pro_sold.aggregate(total_money_sold=Sum('price_sold'))
        total_weight_sold=total_weight_sold['total_weight_sold']
        total_money_sold=total_money_sold['total_money_sold']
        if total_weight_sold>=1000:
            total_weight_sold=total_weight_sold/1000
            unit_sold='KG'
        else:
            unit_sold='G'
    else:
        messages.warning(request,'There is No (SOLD) Item')
        pro_sold=None

    sales_summary()
    gold_price_data={'price': 1800.50, 'currency': 'USD', 'unit': 'per ounce'}

    context={

        'products':pro_available,
        'total_weight_available':total_weight_ava,
        'sum_gold_available':sum_gold_available,
        'unit_availabe':unit_available,

        'total_weight_sold':total_weight_sold,
        'sum_gold_sold':sum_gold_sold,
        'unit_sold':unit_sold,
        'total_money_sold':total_money_sold,
        'shops_info':shops_info,

        'users':User.objects.all(),
        'title':'Jewelry',
        'gold_price_data':gold_price_data,
    }
    return render(request,'pages/dashboard.html',context)


@login_required(login_url='signin')
def mainShops(request):
    pass

@login_required(login_url='signin')
def main_number_Details(request,shop_id):
    pass

@login_required(login_url='signin')
def show_number(request,shop_id,class_):
    pass

@login_required(login_url='signin')
def main_number_Details_sold(request):
    pass

@login_required(login_url='signin')
def show_number_sold(request,class_):
    pass

def sales_summary():
    today = date.today()
    yesterday = datetime.now() - timedelta(days=1)
    start_of_week = today - timedelta(days=today.weekday())
    print('today',today)

    # daily_sales =Products.objects.filter(date_sold=today).aggregate(total_sales=Sum('quantity_sold'))
    # monthly_sales = Products.objects.filter(date_sold__month=today.month, date_sold__year=today.year).aggregate(total_sales=Sum('quantity_sold'))
    # yearly_sales = Products.objects.filter(date_sold__year=today.year).aggregate(total_sales=Sum('quantity_sold'))

    daily_sales =Products.objects.filter(sell_time__date=today,status__name='sold').count()
    weekly_sales = Products.objects.filter(sell_time__gte=start_of_week, creation_time__lte=today,status__name='sold').count()
    monthly_sales = Products.objects.filter(sell_time__month=today.month, creation_time__year=today.year,status__name='sold').count()
    yearly_sales = Products.objects.filter(sell_time__year=today.year,status__name='sold').count()
    print(daily_sales,weekly_sales,monthly_sales,yearly_sales)
    
    return daily_sales,weekly_sales, monthly_sales, yearly_sales,


def main_shops():

    shops_info = [] #list
    # shops_and_staff = {} #dectionary
    all_shops =Shop.objects.all().order_by('startWork')

    if all_shops: # to display all products with employees
        for shop in all_shops:
            weight_gold=0
            weight_percentage=0
            unit=''
            staff_members = shop.staff.all()
            gold_number=shop.shop_pro.filter(status__name='available').count()
            weight_gold,_ = gold24(shop) 
            if weight_gold:
                weight_percentage=calculate_percentage(weight_gold,10)
                if weight_gold>1000:
                    weight_gold=weight_gold/1000
                    unit='KG'
                else:
                    unit='G'
            shops_info.append({
                'shop':shop,
                'staff_members':staff_members,
                'gold_number':gold_number,
                'weight_gold':weight_gold,
                'weight_percentage':weight_percentage,
                'unit':unit,
                })
    return shops_info

# def get_gold_price(request):
#     # يمكنك استبدال هذه البيانات بالبيانات الفعلية من مصدر البيانات الذي تستخدمه
#     gold_price_data = {'price': 1800.50}
#     return JsonResponse(gold_price_data)

def calculate_percentage(desired, total):
    return round((desired / total) * 100,1)/1000

def gold24(shop): 
    #return Gold as 24
    classes=Classes.objects.all()
    total_weight_ava=0
    sum_gold_available=0
    if classes:
        for cl in classes:
            if Products.objects.filter(classes__name=cl.name,status__name='available',shop__name=shop.name,shop__address=shop.address).exists():
                pro_available=Products.objects.filter(classes__name=cl.name,status__name='available',shop__name=shop.name,shop__address=shop.address)

                sum_gold_available+=pro_available.count()
                if cl.name=='24':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp =total_weight_ava_temp['total_weight_ava']*1
                    total_weight_ava+= total_weight_ava_temp* 1

                    # print('total_weight_ava$$$',total_weight_ava)
                elif cl.name=='22':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.916)

                elif cl.name=='21':
                    # print('cl:',cl.name)
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.975)

                elif cl.name=='18':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.875)

                elif cl.name=='14':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp*Decimal(0.585)

                elif cl.name=='8':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp*Decimal(0.333)
                else:
                    total_weight_ava = pro_available.aggregate(total_weight_ava=Sum('weight'))    

    return round(total_weight_ava,4),sum_gold_available

def detailPros(products):
    classes=Classes.objects.all()
    total_weight_ava=0
    sum_gold_available=0
    cash=0
    list_class={}
    if classes:
        for cl in classes:
            if products.filter(classes__name=cl.name,status__name='available').exists():
                pro_available=products.filter(classes__name=cl.name,status__name='available')
  
                sum_gold_available+=pro_available.count()
                if cl.name=='24':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp =total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+= total_weight_ava_temp* 1
                    
                    # print('total_weight_ava$$$',total_weight_ava)
                elif cl.name=='22':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.916)

                elif cl.name=='21':
                    # print('cl:',cl.name)
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.975)

                elif cl.name=='18':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp* Decimal(0.875)

                elif cl.name=='14':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp*Decimal(0.585)

                elif cl.name=='8':
                    total_weight_ava_temp = pro_available.aggregate(total_weight_ava=Sum('weight'))
                    total_weight_ava_temp=total_weight_ava_temp['total_weight_ava']
                    total_weight_ava+=total_weight_ava_temp*Decimal(0.333)
                else:
                    total_weight_ava = pro_available.aggregate(total_weight_ava=Sum('weight'))

                list_class[cl.name]=total_weight_ava_temp

        if products.filter(status__name='sold').exists():
            pro_sold=products.filter(status__name='sold')
            total_price_temp = pro_sold.aggregate(total_price_sold=Sum('price_sold'))
            cash=total_price_temp['total_price_sold']
    print(list_class)
    return round(total_weight_ava,4),sum_gold_available,list_class,cash



@login_required(login_url='signin')
def all_Staff(request,shop_id):
    pass

@login_required(login_url='signin')
def about(request):
    return render(request,'pages/about.html')

def rtl(request):
    return render(request,'rtl.html')