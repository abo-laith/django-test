from django.urls import path
from . import views

urlpatterns=[
    path('products/',views.products,name='products'),
    path('<int:pro_id>',views.product,name='product'),
    path('search',views.search,name='search'),
    path('classes/',views.classes,name='classes'),
    path('types/',views.types,name='types'),
    path('shops',views.shops,name='shops'),
    path('status',views.status,name='status'),
    path('update_product/<int:pro_id>',views.update_product,name='update_product'),
    path('addProduct',views.addProduct,name='addProduct'),
    path('type/remove/<int:removetype_id>',views.remove_form_type,name='remove_from_type'),
    path('classes/remove/<int:removeclass_id>',views.remove_form_class,name='remove_from_class'),
    path('status/remove/<int:removestatus_id>',views.remove_form_status,name='remove_from_status'),
    path('shop/remove/<int:removeshop_id>',views.remove_form_shop,name='remove_from_shop'),
    path('remove/<int:removepro_id>',views.remove_form_pro,name='remove_from_pro'),
    path('delete/<int:pro_id>',views.delete,name='delete'),
    path('addType/',views.addType,name='addType'),
    path('addClass/',views.addClass,name='addClass'),
    path('addstatus/',views.addStatus,name='addStatus'),
    path('addshop/',views.addShop,name='addshop'),
    path('editProducts',views.editProducts,name='editProducts'),
    

]

