from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Products,Classes,Types,Shop,Status,UpdateProducts
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    list_display=['name','barcode','pin','weight','seller','shop','price_sold','status','classes','is_active']
    # list_display_links=['weight','price_sold']
    list_editable=['pin','shop','weight','seller','shop', 'price_sold','status','classes','is_active']
    # search_fields=['name']
    # list_filter=['state']
    # fields=['name','']

class ClassessAdmin(admin.ModelAdmin):
    list_display=['name','price']
    list_editable=['price']

class TypeAdmin(admin.ModelAdmin):
    list_display=['name']
    list_editable=['name',]


admin.site.register(Products,ProductAdmin)
admin.site.register(Classes,ClassessAdmin)
admin.site.register(Types)
admin.site.register(Status)
admin.site.register(Shop)
admin.site.register(UpdateProducts)