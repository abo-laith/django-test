from django.urls import path
from . import views

urlpatterns=[

    path('signin',views.signin,name='signin'),
    path('signup',views.signup,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('profile_staff/<int:staff_id>',views.profile_staff,name='profile_staff'),
    path('logout/',views.logout,name='logout'),
    path('newUser/',views.newUser,name='newUser'),
]
