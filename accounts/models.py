from django.db import models
from django.contrib.auth.models import User
from products.models import Shop
from PIL import Image

class UserProfile(models.Model):

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    shop=models.ForeignKey(Shop,on_delete=models.CASCADE,related_name='staff', blank=True, null=True)
    
    position =models.CharField(max_length=50,null=True,default='Employee',verbose_name='Position:')
    address =models.CharField(max_length=50,null=True,default='Köllner St',verbose_name='Address:')
    city=models.CharField(max_length=50,null=True,default='Düsseldorf',verbose_name='City:')
    state=models.CharField(max_length=50,null=True,default='NRW',verbose_name='State:')
    zip_nummber=models.CharField(max_length=50,null=True,default='111',verbose_name='Zip Number:')
    description=models.TextField(null=True, blank=True, default='Hi, I’m user, Decisions: this is a place to add desc about you')
    mobile = models.CharField(max_length=15,default='+49 1231234123', blank=True, null=True)
    twitter_profile = models.URLField(default='',blank=True, null=True)
    facebook_profile = models.URLField(default='',blank=True, null=True)
    instagram_profile = models.URLField(default='',blank=True, null=True)
    image=models.ImageField(default='default.jpg', upload_to='profile_pics/%Y%m/%d')
    def __str__(self):
        return self.user.username
    
    def save(self):
        super().save()
        img=Image.open(self.image.path)
        if img.width > 300 or img.height > 300 :
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)