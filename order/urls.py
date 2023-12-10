from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('process-order/<int:pk>/', views.process_order, name='process_order'),
    path('order-confirmation/<int:pk>/', views.order_confirmation, name='order_confirmation'),
    path('order-list/', views.order_list, name='order_list'),
    path('order-detail/<int:pk>/', views.order_detail, name='order_detail'),
]
