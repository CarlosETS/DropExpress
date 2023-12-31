from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('product-registration/', views.product_registration, name='product_registration'),
    path('product-registration/create/', views.product_create, name='product_create'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-update/<int:pk>', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('search-by-type/<str:type>/', views.search_by_type, name='search_by_type'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),
]
