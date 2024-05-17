from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages

from pages.views import main_shops
from .models import Products,Types,Classes,Status,Shop
from .froms import UpdateProduct
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from datetime import datetime,timedelta,date
from pages.views import detailPros
from django.contrib.auth.models import User


@login_required(login_url='signin')
def products(request):
    if request.user.is_authenticated:
        print('pagination1111111111111')
        products=Products.objects.all()
        shops=Shop.objects.all()
        shop=None
        cash=0
        name_address=''
        barcode=None
        inputStatus=None
        weightS=None
        weightE=None
        priceS=None
        priceE=None
        cs=None

        if 'cs'in request.GET:
                cs=request.GET['cs']
                if not cs:
                    cs='off'
        
        if 'searchName' in request.GET:
            searchName=request.GET.get('searchName')
            print(searchName,'nameeeeeeee')

            if searchName:

                if is_decimal(searchName):
                    print(isinstance(float(searchName), float))
                    if products.filter(weight=searchName):
                        products=products.get(weight=searchName)
                    
                # if products.filter(name__contains=searchName):
                #     print(111111111111111111111)
                #     products=products.filter(name__contains=searchName)

                if products.filter(barcode__contains=searchName):   
                    products=products.filter(barcode__contains=searchName)
                else:
                    messages.info(request,f'there is No product with ({searchName})')
                    return redirect('products')
                    
        if 'inputBarcode' in request.GET:
            barcode=request.GET.get('inputBarcode')
            if barcode:
                if cs=='on':
                        products=products.filter(barcode__contains=barcode)
                else:   
                    products=products.filter(barcode__icontains=barcode)

        if 'inputName' in request.GET:
            name=request.GET.get('inputName')
            if name:
                if cs=='on':
                        products=products.filter(name__contains=name)
                else:   
                    products=products.filter(name__icontains=name)                    
        
        if 'inputSWeight' in request.GET and 'inputEWeight' in request.GET:
            weightS=request.GET['inputSWeight']
            weightE=request.GET['inputEWeight']
            if weightS and weightE:
                print('weight...')
                if is_decimal(weightS) and is_decimal(weightE):

                    products=products.filter(weight__gte=weightS , weight__lte=weightE)
            else:
                if 'inputSWeight' in request.GET:
                    weightS=request.GET['inputSWeight']
                    if weightS:
                        if is_decimal(weightS):
                            print('floattttttttttt')
                            products=products.filter(weight=weightS)
            
        if 'inputSPrice' in request.GET and 'inputEPrice' in request.GET:
            
            priceS=request.GET['inputSPrice']
            priceE=request.GET['inputEPrice']
            if priceS and priceE:
                print('price...')    
                if is_decimal(priceS) and is_decimal(priceS):
                    products=products.filter(price_sold__gte=priceS,price_sold__lte=priceE)
            else:
                if 'inputSPrice' in request.GET:
                    priceS=request.GET['inputSPrice']
                    if priceS:
                        if is_decimal(priceS):
                            products=products.filter(price_sold=priceS)

        if 'inputShops' in request.GET:
            shops=Shop.objects.all()
            name_address=request.GET.get('inputShops')
            if name_address and name_address!='---':
                name_address=request.GET['inputShops'].split('-')
                print('name_address=',name_address)
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    products=products.filter(shop=shop)

        if 'inputClass' in request.GET:
            inputClass=request.GET.get('inputClass')
            if inputClass:
                classes=Classes.objects.all()
                if  inputClass  in [ x.name for x in classes]:
                    clas=Classes.objects.get(name=inputClass)
                    products=products.filter(classes=clas)
        
        if 'inputType' in request.GET:
            inputType=request.GET.get('inputType')
            if inputType:
                ty=Types.objects.all()
                if  inputType  in [ x.name for x in ty]:
                    types=Types.objects.get(name=inputType)
                    products=products.filter(types=types)

        if 'inputStatus' in request.GET:
            inputStatus=request.GET.get('inputStatus')
            if inputStatus and inputStatus!='---':
                st=Status.objects.all()
                if  inputStatus  in [ x.name for x in st]:
                    status=Status.objects.get(name=inputStatus)
                    products=products.filter(status=status)
                    print('today sold',products)
        
        if 'inputSDate' in request.GET and 'inputEDate' in request.GET:
            inputSDate=request.GET['inputSDate']
            inputEDate=request.GET['inputEDate']
            print(inputSDate,'daaaaaaaaaaa')
            if inputSDate and inputEDate:
                print('Date...')
                if is_date(inputSDate) and is_date(inputEDate):
                    startdate = datetime.strptime(inputSDate, '%Y-%m-%d')
                    specific_date2 = datetime.strptime(inputEDate, '%Y-%m-%d')
                    endDate=specific_date2 + timedelta(days=1)
                    print(startdate,'________',endDate)
                    if inputStatus=='sold':# if search about sold products
                        print('sooososooooosooooos',inputStatus)
                        products=products.filter(sell_time__gte=startdate,sell_time__lte=endDate)
                    else:
                        products=products.filter(creation_time__gte=startdate,creation_time__lte=endDate)
                else:
                    messages.error(request,'there is error in date')
            else:
                if inputSDate:
                    if is_date(inputSDate):
                        specific_date = datetime.strptime(inputSDate, '%Y-%m-%d')
                        if inputStatus=='sold':# if search about sold products
                            products=products.filter(sell_time__date=specific_date)
                        else:
                            products=products.filter(creation_time__date=specific_date)
        
        if request.method == 'POST':
            name_address=request.POST['inputSh'].split('-')
            if name_address and name_address!='---':
               
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    products = Products.objects.filter(shop=shop)
                else:
                    messages.info(request,'في حال لم يتم اختيار فرع سيتم، عرض مبيعات كل الأفرع')
        else:
            messages.info(request,'في حال لم يتم اختيار فرع سيتم، عرض مبيعات كل الأفرع')
       
        weight24,no24,dict,cash=detailPros(products)

        paginator=Paginator(products,20)
        page=request.GET.get('page')
        try:
            products_list=paginator.page(page)
        except PageNotAnInteger:
             products_list=paginator.page(1)
        except EmptyPage:
             products_list=paginator.page(paginator.num_page)

        context={
            'weight24':weight24,
            'no24':no24,
            'dict_details':dict,
            'shops':shops,
            'shop':shop,
            'cash':cash,

            'products':products,
            'products_list':products_list,
            'page':page,
            'title':'Products',
        }
        return render(request,'products/products.html',context)
    else:
        messages.error(request,'you must log in')
        return redirect('signin')

@login_required(login_url='signin')
def product(request,pro_id):

    if request.user.is_authenticated:
        pro=get_object_or_404(Products,pk=pro_id)
        print(pro,'tttttttttttttttttttttt')
        types=Types.objects.all()
        classes=Classes.objects.all()
        context={
            'pro':pro,
            'types':types,
            'classes':classes,
            'title':pro.name,
        }
        return render(request,'products/product.html',context)
    else:
        messages.error(request,'you must log in')
        return redirect('signin')

@login_required(login_url='signin')
def update_product(request,pro_id):

    if request.user.is_authenticated and not request.user.is_anonymous:
        print('......')
        context=None
        x= None
        y=None
        cl= Classes.objects.all()
        ty=Types.objects.all()
        status=Status.objects.all()
        shops=Shop.objects.all()
        pro=Products.objects.get(pk=pro_id)
        if pro.status.name=='sold':
                messages.error(request,'can not Update because (SOLD)')
                return redirect('products')
        
        product_form=UpdateProduct(request.POST,request.FILES, instance=pro)
        context={
                    'title':'updateproduct',
                    'product_form':product_form,
                    'classes':cl,
                    'types':ty,
                    'pro':pro,
                    'status':status,
                    'shops':shops,
                }

        if request.method=='POST' and 'btnOk' in request.POST:

            terms=None
            if request.POST['inputBarcode'] and request.POST['inputName'] and request.POST['inputWeight'] and request.POST['inputClasses']and request.POST['inputTypes']and request.POST['inputStatus']and request.POST['inputSize'] :
                
                pro.barcode=request.POST['inputBarcode']
                pro.name=request.POST['inputName']
                
                if  is_decimal(request.POST['inputWeight']):
                    pro.weight=request.POST['inputWeight']
                else:
                    print('error')
                    messages.error(request,'Weight Number must be digit and smaller than 6')
                    return redirect(f'/products/update_product/{pro_id}')
                
                if  is_decimal(request.POST['inputSize']):
                    pro.size=request.POST['inputSize']
                else:
                    messages.error(request,'Size Number must be digit and smaller than 6')
                    return redirect(f'/products/update_product/{pro_id}')
                    
                if  request.POST['inputClasses']  in [ x.name for x in cl]:
                    pro.classes=Classes.objects.get(name=request.POST['inputClasses'])
                else:
                    print('error')
                    messages.error(request,'Classes  must be in List')
                    return redirect(f'/products/update_product/{pro_id}')                    

                if  request.POST['inputTypes'] in [y.name for y in ty]:
                    pro.types=Types.objects.get(name=request.POST['inputTypes'])
                else:
                    print('error')
                    messages.error(request,'Type  must be in List')
                    return redirect(f'/products/update_product/{pro_id}')                    

                if  request.POST['inputStatus'] in [z.name for z in status]:
                    print('111111',Status.objects.get(name=request.POST['inputStatus']))
                    pro.status=Status.objects.get(name=request.POST['inputStatus'])
                else:
                    print('error')
                    messages.error(request,'Status  must be in List')
                    return redirect(f'/products/update_product/{pro_id}')
                
                
                name_address=request.POST['inputShops'].split('-')
                print('name_address',name_address)
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    # name_address=request.POST['inputShops'].split('-')
                    pro.shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                else:
                    print('error')
                    messages.error(request,'Shops  must be in List')
                    return redirect(f'/products/update_product/{pro_id}')
                    

                pro.description=request.POST['inputDescription']

                if 'terms' in request.POST: 
                    terms=request.POST['terms']

                product_form=UpdateProduct(request.POST,request.FILES, instance=pro)
                
                if product_form.is_valid:
                    if terms == 'on':
                        product_form.save()
                    else:
                        messages.warning(request,'warning you must checked ')
                        return redirect(f'/products/update_product/{pro_id}')
                    
                    messages.success(request,'update has done')
                    return redirect('products')
                else:
                    product_form=UpdateProduct(instance=pro)
          
                context={
                    'title':'updateproduct',
                    'product_form':product_form,
                    'classes':cl,
                    'types':ty,
                    'pro':pro,
                    'status':status,
                    'shops':shops,
                }
          
                return render(request,'products/product_update.html',context)
            else:
                messages.error(request,'Check the Value')
                return render(request,'products/product_update.html',context)
        else:
            return render(request,'products/product_update.html',context)
    
    else:
        messages.error(request,'pls log in')
        return redirect('signin')

@login_required(login_url='signin')
def addProduct(request):
     #variable field
    cl= Classes.objects.all()
    ty=Types.objects.all()
    status=Status.objects.all()
    shops=Shop.objects.all()
    
    context=None
    inputBarcode =None
    inputName='schmetterling'
    inputWeight=None
    inputClasses=None
    inputTypes=None
    inputShop=None
    inputStatus=None
    inputSize=10
    inputDescription=None
    terms=None
    pin=0
    addProduct_form=UpdateProduct(request.POST,request.FILES,)
    lastPro=Products.objects.last()
    if lastPro:
        pin=lastPro.id+1
    else:
        pin=0
    if request.method=='POST' and 'btnSave' in request.POST:
        if 'inputBarcode' in request.POST: inputBarcode=request.POST['inputBarcode']
        else: messages.error(request,'Error in BarCode')
        if 'inputName' in request.POST: inputName=request.POST['inputName']
        else:messages.error(request,'Error in Name')
        if 'inputWeight' in request.POST: inputWeight=request.POST['inputWeight']
        else: messages.error(request,'Error in Weight')
        if 'inputClasses' in request.POST: inputClasses=request.POST['inputClasses']
        else: messages.error(request,'Error in Classes')
        if 'inputTypes' in request.POST: inputTypes=request.POST['inputTypes']
        else:messages.error(request,'Error in Types')
        if 'inputShop' in request.POST: inputShop=request.POST['inputShop']
        else:messages.error(request,'Error in Shop')
        if 'inputStatus' in request.POST:inputStatus=request.POST['inputStatus']
        else: messages.error(request,'Error in Status')
        if 'inputSize' in request.POST:inputSize=request.POST['inputSize']
        else: messages.error(request,'Error in Size')
        if 'inputDescription' in request.POST: inputDescription=request.POST['inputDescription']
        else:messages.error(request,'error in Description')
        if 'terms' in request.POST: terms=request.POST['terms']
        
        if inputBarcode  and inputWeight and inputClasses and inputTypes and inputStatus and inputShop:
            if terms =='on':
                name_address=inputShop.split('-')
                if Products.objects.filter(barcode=inputBarcode).exists() or not inputBarcode.isalnum():
                    messages.error(request,'this barcode is token Or must be Number Or barcode contain space ')
                else:
                    if not is_decimal(inputWeight) or ' ' in request.POST['inputWeight']:
                        messages.error(request,'Error in Weight Or contain space Or < 0')
                    else:
                        if not is_decimal(inputSize) or ' ' in request.POST['inputSize']:
                            messages.error(request,'Error in Size or contain space')
                        else:
                            if not inputStatus in [z.name for z in status]:
                                messages.error(request,'error with Status')
                            else:
                                if not inputTypes in [x.name for x in ty]:
                                    messages.error(request,'error with Type')
                                else:
                                    if not (len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops]):
                                        messages.error(request,f'error with Shop{name_address}')
                                    
                                    else:
                                        if not inputClasses in [w.name for w in cl]:
                                            messages.error(request,'error with Class')
                                        else:
                                            if not inputName.isalnum():
                                                messages.error(request,'Name must be Number Or barcode contain space')
                                            else:
                                                
                                                inputName+='*'
                                                inputClasses=Classes.objects.get(name=inputClasses)
                                                inputTypes=Types.objects.get(name=inputTypes)
                                                inputStatus=Status.objects.get(name=inputStatus)
                                                print('inputShop=',inputShop)
                                                inputShop=Shop.objects.get(name=name_address[0],address=name_address[1])
                                                product=Products(
                                                    user=request.user,
                                                    classes=inputClasses,
                                                    types=inputTypes,
                                                    status=inputStatus,
                                                    shop=inputShop,
                                                    barcode=inputBarcode,
                                                    pin=pin,
                                                    name=inputName,
                                                    size=inputSize,
                                                    weight=inputWeight,
                                                    description=inputDescription,  
                                                )
                                                addProduct_form=UpdateProduct(request.POST,request.FILES,instance=product)
                                                addProduct_form.save()
                                                messages.success(request,'Success to add new Product')
                                                return redirect('products')
            else:
                messages.error(request,'Error you must agree to the Terms')
        else:
            print('ppppppppppppppppppp',inputBarcode)
            if inputBarcode=='':
                messages.error(request,'Barcode must not be Empty!')
            if inputWeight=='':
                messages.error(request,'Weight must not be Empty!')
            messages.error(request,'Error empty fields')
    else:
        # not POST
        context={
            'addProduct_form':addProduct_form,
            'classes':cl,
            'types':ty,
            'status':status,
            'shops':shops,
            'name':inputName,
            'pincode':pin,
            'size':inputSize,
            'title':'New Product'

            }
        return render(request,'products/addProduct.html',context)
    context={
            'title':'updateproduct',
            'addProduct_form':addProduct_form,
            'classes':cl,
            'types':ty,
            'status':status,
            'shops':shops,
            'barcode':inputBarcode,
            'name':inputName,
            'weight':inputWeight,
            'size':inputSize,
            'description':inputDescription,
            'title':'New Product'
            }
    return render(request,'products/addProduct.html',context)

@login_required(login_url='signin')
def search(request):

    name_address=''
    barcode=None
    inputStatus=None
    st=None
    ty=None
    clas=None
    shop=None
    cash=0
    inputStaff=None
    staff=None
    weightS=None
    weightE=None
    priceS=None
    priceE=None
    cs=None

    products=Products.objects.all()
    
    classes=Classes.objects.all()
    types=Types.objects.all()
    shops=Shop.objects.all()
    status=Status.objects.all()
    staffs=User.objects.all()

    if request.method == 'GET':

        if 'cs'in request.GET:
                cs=request.GET['cs']
                if not cs:
                    cs='off'
        
        if 'searchName' in request.GET:
            searchName=request.GET.get('searchName')
            print(searchName,'nameeeeeeee')
            if searchName:
                if is_decimal(searchName):
                    print(isinstance(float(searchName), float))
                    if products.filter(weight=searchName):
                        products=products.get(weight=searchName)
                if products.filter(barcode__contains=searchName):   
                    products=products.filter(barcode__contains=searchName)
                else:
                    messages.info(request,f'there is No product with ({searchName})')
                    return redirect('products')
                    
        if 'inputBarcode' in request.GET:
            barcode=request.GET.get('inputBarcode')
            if barcode:
                if cs=='on':
                        products=products.filter(barcode__contains=barcode)
                else:   
                    products=products.filter(barcode__icontains=barcode)

        if 'inputName' in request.GET:
            name=request.GET.get('inputName')
            if name:
                if cs=='on':
                        products=products.filter(name__contains=name)
                else:   
                    products=products.filter(name__icontains=name)                    
        
        if 'inputSWeight' in request.GET and 'inputEWeight' in request.GET:
            weightS=request.GET['inputSWeight']
            weightE=request.GET['inputEWeight']
            if weightS and weightE:
                print('weight...')
                if is_decimal(weightS) and is_decimal(weightE):

                    products=products.filter(weight__gte=weightS , weight__lte=weightE)
            else:
                if 'inputSWeight' in request.GET:
                    weightS=request.GET['inputSWeight']
                    if weightS:
                        if is_decimal(weightS):
                            print('floattttttttttt')
                            products=products.filter(weight=weightS)
            
        if 'inputSPrice' in request.GET and 'inputEPrice' in request.GET:
            
            priceS=request.GET['inputSPrice']
            priceE=request.GET['inputEPrice']
            if priceS and priceE:
                print('price...')    
                if is_decimal(priceS) and is_decimal(priceS):
                    print('lllllllllllllll')
                    products=products.filter(price_sold__gte=priceS,price_sold__lte=priceE)
                    print(products.count())

            else:
                if 'inputSPrice' in request.GET:
                    priceS=request.GET['inputSPrice']
                    if priceS:
                        if is_decimal(priceS):
                            print(products,'lllllllllllllll')
                            products=products.filter(price_sold=priceS)
                            print(products,'333333333333333')
       
        if 'inputShops' in request.GET:
            shops=Shop.objects.all()
            name_address=request.GET.get('inputShops')
            if name_address and name_address!='---':
                name_address=request.GET['inputShops'].split('-')
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    products=products.filter(shop=shop)

        if 'inputClass' in request.GET:
            inputClass=request.GET.get('inputClass')
            if inputClass and inputClass!='---':
                classes=Classes.objects.all()
                if  inputClass  in [ x.name for x in classes]:
                    clas=Classes.objects.get(name=inputClass)
                    products=products.filter(classes=clas)
        
        if 'inputType' in request.GET:
            inputType=request.GET.get('inputType')
            if inputType and inputType != '---':
                ty1=Types.objects.all()
                if  inputType  in [ x.name for x in ty1]:
                    ty=ty1.get(name=inputType)
                    products=products.filter(types=ty)

        if 'inputStatus' in request.GET:
            inputStatus=request.GET.get('inputStatus')
            if inputStatus:
                st1=status.all()
                if  inputStatus  in [ x.name for x in st1]:
                    st=st1.get(name=inputStatus)
                    products=products.filter(status=st)
        
        if 'inputSDate' in request.GET and 'inputEDate' in request.GET:
            inputSDate=request.GET['inputSDate']
            inputEDate=request.GET['inputEDate']
            print(inputSDate,'daaaaaaaaaaa')
            if inputSDate and inputEDate:
                print('Date...')
                if is_date(inputSDate) and is_date(inputEDate):
                    startdate = datetime.strptime(inputSDate, '%Y-%m-%d')
                    specific_date2 = datetime.strptime(inputEDate, '%Y-%m-%d')
                    endDate=specific_date2 + timedelta(days=1)
                    print(startdate,'________',endDate)
                    if inputStatus=='sold':# if search about sold products
                        print('sooososooooosooooos',inputStatus)
                        products=products.filter(sell_time__gte=startdate,sell_time__lte=endDate)
                    else:
                        products=products.filter(creation_time__gte=startdate,creation_time__lte=endDate)
                else:
                    messages.error(request,'there is error in date')
            else:
                if inputSDate:
                    if is_date(inputSDate):
                        specific_date = datetime.strptime(inputSDate, '%Y-%m-%d')
                        if inputStatus=='sold':# if search about sold products
                            products=products.filter(sell_time__date=specific_date)
                        else:
                            products=products.filter(creation_time__date=specific_date)
        
        if 'inputStaff' in request.GET:
            inputStaff=request.GET.get('inputStaff')
            if inputStaff:
                if staffs.filter(username=inputStaff).exists():
                    staff=staffs.get(username=inputStaff)
                    products=products.filter(seller=staff)

        weight24,no24,dict,cash=detailPros(products)

        # for pro in products:
        #     pro.name=delete_star_name(pro)
        #     pro.save()

        context={
            'weight24':weight24,
            'no24':no24,
            'dict_details':dict,
            'shops':shops,
            'shop':name_address,
            'cash':cash,
            'products_list':products,
            'classes':classes,
            'types':types,
            'shops':shops,
            'status':status,
            'staffs':staffs,
            'title':'Search',

            'staff':staff,
            'st':st,
            'ty':ty,
            'clas':clas,
            'shop':shop,
            'priceS':priceS,
            'priceE':priceE,

            
        }

      
    else:# not GET
        context={

            'classes':classes,
            'types':types,
            'shops':shops,
            'status':status,
            'title':'Search'
        }

    return render(request,'products/search.html',context)

@login_required(login_url='signin')
def shops(request):
    shops_info=None
    shops_info=main_shops()
    # sh=Shop.objects.all()
    context={
        'shops_info':shops_info,
        # 'shops':sh,
        'title':'Shops'
    }
    return render(request,'products/shops.html',context)

@login_required(login_url='signin')
def status(request):
    st=Status.objects.all()
    context={
        'status':st,
        'title':'status'
    }
    return render(request,'products/status.html',context)

@login_required(login_url='signin')
def classes(request):
    cl=Classes.objects.all()
    
    print(cl)
    context={
        'title':'classes',
        'classes':cl,
    }

    return render(request,'products/classes.html',context)

@login_required(login_url='signin')
def types(request):
    types=Types.objects.all()
    # products=Products.objects.all()
    
    
    context={
        'types':types,
        # 'products':products,
        'title':'Types'
    }
    return render(request,'products/types.html',context)

@login_required(login_url='signin')
def remove_form_type(request,removetype_id):
    if request.user.is_authenticated and not request.user.is_anonymous and removetype_id:
        if not Types.objects.filter(pk=removetype_id).exists():
            return redirect('types')
        type=Types.objects.get(id=removetype_id)
        print('typeeee',types)
        print('type___', 'item' in request.GET)
        products=Products.objects.all().filter(types=type)
        print('prroooo',products)
        context={
        'products':products,
        'type':type,
        'title':'removePro',
        }
        if products:
            messages.warning(request,f'there are many products accociated with this ({type}) you must delete all these Products before delete them' )
            messages.warning(request,f' you can delete Type ({type}) just there is no products')
            return render(request,'products/delete.html',context)
        else:
            messages.warning(request,f'Done you deleted  ({type})')
            type.delete()
            return redirect('types')

        
        # type.delete()
    return render(request,'products/types.html',context)

@login_required(login_url='signin')
def remove_form_class(request,removeclass_id):
    if request.user.is_authenticated and not request.user.is_anonymous and removeclass_id:

        if not Classes.objects.filter(pk=removeclass_id).exists():
            return redirect('classes')
        cl=Classes.objects.get(id=removeclass_id)
        if cl:
            products=Products.objects.all().filter(classes=cl)
            context={
            'products':products,
            'class':cl,
            'title':'removePro',
            }

            if products:
                messages.warning(request,f'there are many products accociated with this ({cl}) you must delete all these Products before delete them' )
                messages.warning(request,f' you can delete Class ({cl}) just there is no products')
                return render(request,'products/delete.html',context)
            else:
                messages.warning(request,f'Done you deleted  ({cl})')
                cl.delete()
                return redirect('classes')
                
        else:
            messages.warning(request,'there is no Pro to delete')
            return redirect('classes')
        
        # type.delete()
    return render(request,'products/classes.html',context)

@login_required(login_url='signin')
def remove_form_status(request,removestatus_id):
    if request.user.is_authenticated and not request.user.is_anonymous and removestatus_id:

        if not Status.objects.filter(pk=removestatus_id).exists():
            return redirect('status')
        st=Status.objects.get(id=removestatus_id)
        if st:
            products=Products.objects.all().filter(status=st)
            context={
            'products':products,
            'status':st,
            'title':'removeStatus',
            }

            if products:
                messages.warning(request,f'there are many products accociated with this ({st}) you must delete all these Products before delete them' )
                messages.warning(request,f' you can delete Status ({st}) just there is no products')
                return render(request,'products/delete.html',context)
            else:
                messages.warning(request,f'Done you deleted  ({st})')
                st.delete()
                return redirect('status')
                
        else:
            messages.warning(request,'there is no Pro to delete')
            return redirect('status')
        
        # type.delete()
    return render(request,'products/status.html',context)

@login_required(login_url='signin')
def remove_form_shop(request,removeshop_id):
    if request.user.is_authenticated and not request.user.is_anonymous and removeshop_id:
        print('remove shop')
        if not Shop.objects.filter(pk=removeshop_id).exists():
            return redirect('shops')
        sh=Shop.objects.get(id=removeshop_id)
        if sh:
            products=Products.objects.all().filter(shop=sh)
            context={
            'products':products,
            'shop':sh,
            'title':'removeShop',
            }

            if products:
                messages.warning(request,f'there are many products accociated with this ({sh}) you must delete all these Products before delete them' )
                messages.warning(request,f' you can delete Shop ({sh}) just there is no products')
                return render(request,'products/delete.html',context)
            else:
                messages.warning(request,f'Done you deleted  ({sh})')
                sh.delete()
                return redirect('shops')
                
        else:
            messages.warning(request,'there is no Pro to delete')
            return redirect('shops')
        
        # type.delete()
    return render(request,'products/classes.html',context)

@login_required(login_url='signin')
def remove_form_pro(request,removepro_id):
    if request.user.is_authenticated and not request.user.is_anonymous and removepro_id:
        products=Products.objects.all()
        context={
            'products_list':products,
            'title':'Prosucts',
            }        
        if not Products.objects.filter(pk=removepro_id).exists():
            messages.warning(request,'there is no Pro to delete')
            return redirect('products')
        pro=Products.objects.get(id=removepro_id)
        if pro:

            if pro.status.name=='sold' or  pro.status.name=='block': # do not able to delete id status Sold
                messages.error(request,'can not delete because (SOLD)')
                return redirect('main_number_details_sold')
            
            messages.warning(request,f'Done you deleted  ({pro.name})')
            pro.delete()
            # type.delete()
            paginator=Paginator(products,5)
            page=request.GET.get('page')
            try:
                products_list=paginator.page(page)
            except PageNotAnInteger:
                products_list=paginator.page(1)
            except EmptyPage:
                products_list=paginator.page(paginator.num_page)

            context={
                'products':products,
                'products_list':products_list,
                'page':page,
                'title':'Products',
            }
            return render(request,'products/products.html',context)
        else:
            messages.warning(request,'there is no Pro to delete')
            return redirect('products')
    else:
        return redirect('products')


@login_required(login_url='signin')
def addType(request):
    if request.method=='POST' and 'inputType' in request.POST and not request.user.is_anonymous:
        types=Types.objects.all()
        context={
                'types':types,
                'title':'Types'
            }
        if not Types.objects.filter(name=request.POST['inputType']).exists():
            inputType=request.POST['inputType']
            type=Types.objects.create(
                name=inputType,
            )
            print('adddddtoooootypeeee',request.POST['inputType'])
            messages.success(request,'success added')
           
            return render(request,'products/types.html',context)
        else:
            messages.error(request,'type is tocken, choose another one')
            return redirect('types')
    else:
        print(':)')
        return redirect('types')

@login_required(login_url='signin')
def addClass(request):
    if request.method=='POST' and 'inputClass' in request.POST and 'inputPrice' in request.POST and not request.user.is_anonymous:
        classes=Classes.objects.all()
        context={
                'classes':classes,
                'title':'Classes'
            }
        if not Classes.objects.filter(name=request.POST['inputClass']).exists():
            inputClass=request.POST['inputClass']
            inputPrice=request.POST['inputPrice']
            classes=Classes.objects.create(
                name=inputClass,
                price=inputPrice,
            )
            print('adddddtoooootypeeee',request.POST['inputClass'])
            messages.success(request,'success added class')
           
            return render(request,'products/classes.html',context)
        else:
            messages.error(request,'class is tocken, choose another one')
            return redirect('classes')
    else:
        print(':)')
        return redirect('classes')

@login_required(login_url='signin')
def addStatus(request):
    print('sdsdsdsd')
    if request.method=='POST' and 'inputStatus' in request.POST and not request.user.is_anonymous:
        status=Status.objects.all()
        context={
                'status':status,
                'title':'Status'
            }
        if not Status.objects.filter(name=request.POST['inputStatus']).exists():
            inputStatus=request.POST['inputStatus']
            status=Status.objects.create(
                name=inputStatus,
            )
            print('adddddtoooootypeeee',request.POST['inputStatus'])
            messages.success(request,'success added Status')
           
            return render(request,'products/status.html',context)
        else:
            messages.error(request,'status is tocken, choose another one')
            return redirect('status')
    else:
        print(':)')
        return redirect('status')

@login_required(login_url='signin')
def addShop(request):
    if request.method=='POST' and 'inputShop' in request.POST and 'inputAddress' in request.POST and not request.user.is_anonymous:
        # shops=Shop.objects.all()
        
       
        if not Shop.objects.filter(name=request.POST['inputShop']).exists():
            inputShop=request.POST['inputShop']
            inputAddress=request.POST['inputAddress']
            shop=Shop.objects.create(
                name=inputShop,
                address=inputAddress,
            )
            shops_info=main_shops()
            context={
                'shops_info':shops_info,
                'title':'Shops'
            }
            print('adddddtoooootypeeee',request.POST['inputShop'])
            messages.success(request,'success added Shop')
           
            return render(request,'products/shops.html',context)
        else:
            messages.error(request,'class is tocken, choose another one')
            return redirect('shops')
    else:
        print(':)')
        return redirect('shops')

@login_required(login_url='signin')
def delete(request,pro_id):
    
    if not Products.objects.filter(pk=pro_id).exists():
        messages.warning(request,'No product to Delete')
        return redirect('products')
    
    products=Products.objects.all()
    pro=Products.objects.get(pk=pro_id)
    if pro:

        
        
        pro.delete()
        messages.success(request,'done Delete')
    else:
        messages.success(request,'No product to Delete')
    context={
        'products':products,
        'title':'detele',
    }
    return render(request,'products/delete.html',context)

def showproducts(request):
    print(request.GET['btnmodel'])
    context={

    }
    return redirect('products')

def editProducts(request):
    return render(request,'products/editProducts.html')

def is_decimal(txtNumber):
    num=txtNumber.split('.')
    print(num)
    if len(num) == 1:
        if num[0].isdigit():
            print('1digit')
            if len(num[0])>5:
                print('length >5 error')
                return 0
            else:
                
            # return digit
                print('digit and<5')
                return 1    
        else:
            print('1 but not digit')
            return 0
    elif len(num)==2:
        if num[0].isdigit() and num[1].isdigit():
            if len(num[0])>5 and len(num[1]>3):
                print('error length >5 ,>3')
                return 0
            elif len(num[0])<6 and len(num[1])<4:
                print(' digit and <5,<3')
                return 1
            else:
                print('digit2 length error')
                return 0
        else:
            print('2 but not digit')
    else:
        print('no digit error')     
        return 0

def is_date(date):

    # initializing format 
    format = "%Y-%m-%d"
    
    # checking if format matches the date 
    res = True
    
    # using try-except to check for truth value
    try:
        res = bool(datetime.strptime(date, format))
    except ValueError:
        res = False
    
    # printing result
    print("Does date match format? : " + str(res))
    return res

def delete_star_name(pro):

    current_date = date.today()
    difference = pro.creation_time - current_date
    
    if pro.name.endswith('*') and difference > datetime.timedelta(days=1):

        modified_name = pro.name[:-1]
    else:
        modified_name = pro.name
    print()
    return modified_name