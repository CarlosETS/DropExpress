from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product-registration/', views.product_registration, name='product_registration'),
    path('product-registration/create/', views.product_create, name='product_create'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-update/<int:pk>', views.product_update, name='product_update'),
    path('delete/<int:code>/', views.delete_product, name='delete_product'),
]
