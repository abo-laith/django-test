from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),

    path('main_shops',views.mainShops,name='main_shops'),
    path('main_number_details/<int:shop_id>',views.main_number_Details,name='main_number_details'),
    path('show_number/<int:shop_id>/<int:class_>',views.show_number,name='show_number'),

    path('main_number_details_sold',views.main_number_Details_sold,name='main_number_details_sold'),
    path('show_number_sold/<int:class_>',views.show_number_sold,name='show_number_sold'),
    path('all_staff/<int:shop_id>',views.all_Staff,name='all_staff'),
    path('about/',views.about,name='about'),
    path('rtl/',views.rtl,name='rtl'),
]
