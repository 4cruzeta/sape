# inventory/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('<int:pk>/', views.inventory_detail, name='inventory_detail'),
    path('new/', views.inventory_new, name='inventory_new'),
    path('<int:pk>/edit/', views.inventory_edit, name='inventory_edit'),
]