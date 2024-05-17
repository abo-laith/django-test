from django.shortcuts import render
from django.contrib import messages
from products.models import Classes, Products,Types,Shop,Status
from django.contrib.auth.decorators import login_required
from pages.views import detailPros
# Create your views here.
def billing(request):
    
    return render(request,'bills/billing.html')

@login_required(login_url='signin')
def invantory(request):

    weight24=None
    no24=None
    dict=None
    cash=0
    products=None
    products_list=None
    inputShop=None
    inputClasses=None
    
    inputType=None
    inputStatus=None
    inputInvantory=None
    inputInvantory_before=''
    inputSDate=None
    inputEDate=None
    name_address=None
    shop=None
    clas=None
    ty=None
    st=None

    products=Products.objects.all()
    classes=Classes.objects.all()
    types=Types.objects.all()
    shops=Shop.objects.all()
    status=Status.objects.all()

    if request.method=='POST':

        if 'inputShops' in request.POST:
            name_address=request.POST['inputShops'].split('-')
            print('aaaaaaaaaaa',name_address)
            if name_address:
                if len(name_address)==2 and  name_address[0]in [c.name for c in shops]and name_address[1]in [a.address for a in shops] :
                    shop=Shop.objects.get(name=name_address[0],address=name_address[1])
                    products=products.filter(shop__name=name_address[0],shop__address=name_address[1])
        
        if 'inputClass' in request.POST :
            inputClasses=request.POST['inputClass']
            if inputClasses and inputClasses!='---':
                classes=Classes.objects.all()
                if  inputClasses  in [ x.name for x in classes]:
                    clas=Classes.objects.get(name=inputClasses)
                    products=products.filter(classes=clas)

        if 'inputType' in request.POST:
            inputType=request.POST['inputType']
            if inputType and inputType != '---':
                ty1=Types.objects.all()
                if  inputType  in [ x.name for x in ty1]:
                    ty=ty1.get(name=inputType)
                    products=products.filter(types=ty)

        if 'inputStatus' in request.POST:
            inputStatus=request.POST['inputStatus']
            if inputStatus and inputStatus!='---':
                st=Status.objects.all()
                if  inputStatus  in [ x.name for x in st]:
                    st=Status.objects.get(name=inputStatus)
                    products=products.filter(status=st)
                    print('today sold',products)

        if 'inputInvantory' in request.POST:
            inputInvantory_before=request.POST.get('inputInvantory')
            print('inventory_before',inputInvantory_before)
            inputInvantory=request.POST.get('inputInvantory','').split('\n')

            inputSDate=request.POST.get('inputSDate')
            inputEDate=request.POST.get('inputEDate')
            if inputInvantory !='':
                print('inputInvantory1',inputInvantory)
                # Remove any empty strings or whitespace
                inputInvantory = [barcode.strip() for barcode in inputInvantory if barcode.strip()] # to The strip() method in Python is used to remove leading and trailing whitespace (spaces, tabs, and newline characters) from a string
                print('inventory aftre= ',inputInvantory)
                print('inventory aftre= ',products.filter(barcode__in=inputInvantory),'   ',products.filter(barcode__in=inputInvantory).count())
                products_list=products.filter(barcode__in=inputInvantory)

                print(detailPros(products_list))

                weight24,no24,dict,cash=detailPros(products_list)
                print('nnnnnnnnnn',cash)
                print('dict',detailPros(products_list))

        context={
        'weight24':weight24,
        'no24':no24,
        'dict_details':dict,
        'cash':cash,
        'products_list':products_list,
        'inventory':inputInvantory_before,

        'shop':shop,
        'class':clas,
        'ty':ty,
        'st':st,

        'type':inputType,
        'stat':inputStatus,

        'classes':classes,
        'types':types,
        'shops':shops,
        'status':status,
        'title':'Invantory'
        }

        return render(request,'bills/invantory.html',context)
    else:
        messages.info(request,'انتباه وشوية حزر: في حال لم تدخل قيم في الحقول سيتم جلب اي قيمة في أي المحلات')
        messages.info(request,'انتباه وشوية حزر: input Inventory')

        context={
            'shop':shop,

            'classes':classes,
            'types':types,
            'shops':shops,
            'status':status,
            'title':'Invantory'
        }
        return render(request,'bills/invantory.html',context)