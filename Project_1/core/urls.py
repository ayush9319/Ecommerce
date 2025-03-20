from django.urls import path
from core import views

urlpatterns = [
    path('',views.log_in,name="login"),
    path('sign/',views.sign_up,name="signup"),
    path('logout/',views.log_out,name='logout'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_page/',views.admin_page,name='admin_page'),
    path('admin_customer/',views.admin_customer,name='admin_customer'),
    path('products/',views.product_admin,name='product_admin'),
    path('admin_products/',views.admin_products ,name='admin_products'),
    path('delete/',views.delete_product, name="delete"),
    path('edit/',views.edit_product, name="edit")
]
