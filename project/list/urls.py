from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_store/', views.add_store, name='add_store'),
    path('add_purchase/', views.add_purchase, name='add_purchase'),
    path('add_user/', views.add_user, name='add_user'),
    path('report/', views.monthly_report, name='monthly_report'),
    path('my_purchases/', views.my_purchases, name='my_purchases'),
]