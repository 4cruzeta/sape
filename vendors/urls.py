# vendors/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('new/', views.vendor_new, name='vendor_new'),
    path('<int:pk>/edit/', views.vendor_edit, name='vendor_edit'),
    path('<int:pk>/products/', views.vendorproduct_list, name='products'),
    path('<int:pk>/products/<int:vendorproduct_pk>/', views.vendorproduct_detail, name='vendorproduct_detail'),
    path('<int:pk>/products/new/', views.vendorproduct_new, name='vendorproduct_new'),
    path('<int:pk>/products/<int:vendorproduct_pk>/edit/', views.vendorproduct_edit, name='vendorproduct_edit'),
    
]