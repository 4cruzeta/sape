# vendors/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.vendor_list, name='vendor_list'),
    path('<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('new/', views.vendor_new, name='vendor_new'),
    path('<int:pk>/edit/', views.vendor_edit, name='vendor_edit'),
    path('<int:pk>/delete/', views.vendor_delete, name='vendor_delete'),
    path('<int:pk>/products/', views.vendorproduct_list, name='products'),
    path('<int:pk>/products/<int:vendorproduct_pk>/', views.vendorproduct_detail, name='vendorproduct_detail'),
    path('<int:pk>/products/new/', views.vendorproduct_new, name='vendorproduct_new'),
    path('<int:pk>/products/<int:vendorproduct_pk>/edit/', views.vendorproduct_edit, name='vendorproduct_edit'),
    path('<int:pk>/products/<int:vendorproduct_pk>/delete/', views.vendorproduct_delete, name='vendorproduct_delete'),
    path('<int:vendor_id>/orders/', views.vendor_order_list, name='vendor_order_list'),
    path('<int:vendor_id>/orders/new/', views.vendor_order_new, name='vendor_order_new'),
    path('<int:vendor_id>/orders/<int:order_id>/delete/', views.vendor_order_delete, name='vendor_order_delete'),
]