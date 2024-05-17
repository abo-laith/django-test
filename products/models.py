# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image 
from datetime import datetime,timedelta
# Create your models here.

class Shop(models.Model):
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=50)
    startWork=models.DateTimeField(default=datetime.now)
    update_time=models.DateTimeField(default=datetime.now)
    desc=models.CharField(max_length=50,null=True,default='kette',verbose_name='Name: ')
    def __str__(self):
        return self.name.capitalize() + '  '+self.address.capitalize()
    class Meta:
         ordering=['name']

class Classes(models.Model):
    name=models.CharField(max_length=50,default='21',unique=True)
    price=models.DecimalField(max_digits=6,decimal_places=2,verbose_name='Price $')
    creation_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(default=datetime.now)

    Conversion_ratio=models.CharField(max_length=50, null=True,blank=True,default=0)
    desc=models.CharField(max_length=100,null=True,default='',verbose_name='Desc: ')

    def __str__(self):
        return self.name +' '+ str(self.price)

class Types(models.Model):
    name=models.CharField(max_length=50,default='ring',unique=True)
    update_time=models.DateTimeField(default=datetime.now)
    desc=models.CharField(max_length=100,null=True,default='',verbose_name='Desc: ')
    def __str__(self):
        return self.name
    
class Status(models.Model):
    name=models.CharField(max_length=50,default='available',unique=True)
    update_time=models.DateTimeField(default=datetime.now)
    desc=models.CharField(max_length=100,null=True,default='',verbose_name='Desc: ')
    def __str__(self):
        return self.name.capitalize()
    class Meta:
        ordering=['name']


class Products(models.Model):

    user=models.ForeignKey(User,on_delete=models.PROTECT,related_name='user_pro', )# User creation
    seller=models.ForeignKey(User,on_delete=models.PROTECT,related_name='seller_pro', )# User seller
    classes=models.ForeignKey(Classes,on_delete=models.CASCADE,related_name='class_pro',)
    types=models.ForeignKey(Types,on_delete=models.PROTECT,related_name='type_pro', )
    status=models.ForeignKey(Status,on_delete=models.PROTECT,related_name='status_pro', )
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='shop_pro', )

    barcode=models.CharField(max_length=50,unique=True,verbose_name='BarCode:', default='123123123')
    pin=models.CharField(max_length=10,unique=True ,verbose_name='PinCode:',default='123456')
    name=models.CharField(max_length=50,null=True,default='kette',verbose_name='Name: ')
   

    size=models.IntegerField(null=True,default=10)
    price_sold=models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True,default=0,verbose_name='Sold Price $:')
    weight=models.DecimalField(max_digits=7,decimal_places=3,default=10 ,verbose_name='Weight G:')
 
    
    is_quantity=models.BooleanField(default=False)
    
    is_active=models.BooleanField(default=True)
    desc=models.CharField(max_length=100,null=True,default='',verbose_name='Desc: ')
    description=models.TextField(null=True, blank=True, default='this is place for description')
    

    creation_time=models.DateTimeField(auto_now_add=True)
    sell_time=models.DateTimeField(default=datetime.now)
    update_time=models.DateTimeField(default=datetime.now)
    image=image=models.ImageField(default='default_pro.jpg',upload_to='products/%Y/%m/%d')

    def __str__(self):
       
        return self.name
    

    def save(self):
        super().save()
        img=Image.open(self.image.path)
        if img.width > 300 or img.height > 300 :
            output_size=(400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
    class Meta:
        ordering=['-creation_time']

class UpdateProducts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='product_update')
    update_time=models.DateTimeField(default=datetime.now)
    desc=models.CharField(max_length=100,null=True,default='',verbose_name='Desc: ')

    def __str__(self):
        return self.product.name
    class Meta:
        ordering=['update_time']
    
    
