from django.urls import path
from . import views

urlpatterns=[
    path('seller',views.seller,name='seller'),
    path('searchpro',views.serachPro,name='searchpro'),
    path('donesell',views.doneSell,name='donesell'),
    path('daily',views.daily_sales,name='daily'),
    path('weekly',views.weekly_sales,name='weekly'),
    path('monthly',views.monthly_sales,name='monthly'),
    path('yearly',views.yearly_sales,name='yearly'),
    
]