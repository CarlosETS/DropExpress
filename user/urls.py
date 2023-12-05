from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('employee-registration/', views.employee_registration, name='employee_registration'),
    path('employee-registration/create/', views.employee_create, name='employee_create'),
    path('employee-list/', views.employee_list, name='employee_list'),
    path('employee-update/<int:pk>', views.employee_update, name='employee_update'),
    path('delete/<int:code>/', views.delete_user, name='delete_user'),
]
