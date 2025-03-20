from django.urls import path
from product_app import views


urlpatterns = [
    path('',views.home,name="home"),
    path('add_product/',views.add_product,name='add_product'),
    path('contact/', views.contact_details,name="contact"),
    path('about/', views.about,name="about"),
    path('profile/', views.profile_details,name="profile"),
    path('product_list/', views.product_list,name="product_list"),
    path('category_products/', views.category_products,name="category_products"),
    path('test/', views.test),
    path('b/', views.product_desc, name='product_desc'),
    path('buying/', views.buying, name='buying'),
    path('cart/', views.cart, name='cart')
]
