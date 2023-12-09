from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('view/', views.view_cart, name='view-cart'),
    path('remove/<int:cart_item_id>/', views.remove_from_cart, name='remove-from-cart'),
]
