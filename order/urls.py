from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('process_order/', views.process_order, name='process_order'),
]
