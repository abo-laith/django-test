from django.urls import path
from . import views

urlpatterns=[
    path('billing/',views.billing,name='billing'),
    path('invantory',views.invantory,name='invantory'),
]