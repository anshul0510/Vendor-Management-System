"""
URL configuration for VendorManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vendors.views import create_vendor,get_vendor,update_vendor,delete_vendor,list_vendors,create_purchase_order,list_purchase_orders,get_purchase_order,update_purchase_order,delete_purchase_order,get_vendor_performance,acknowledge_purchase_order
from rest_framework.authtoken.views import ObtainAuthToken


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api-token-auth'),
    path('api/vendors/',create_vendor, name='create-vendor'),
    path('api/vendors/<int:vendor_id>/',get_vendor, name='get-vendor'),
    path('api/vendors/<int:vendor_id>/update/',update_vendor, name='update-vendor'),
    path('api/vendors/<int:vendor_id>/delete/',delete_vendor, name='delete-vendor'),
    path('api/vendors/all/',list_vendors, name='list-vendors'),
    path('api/purchase_orders/', create_purchase_order, name='create-purchase-order'),
    path('api/purchase_orders/all/', list_purchase_orders, name='list-purchase-orders'),
    path('api/purchase_orders/<int:po_id>/', get_purchase_order, name='get-purchase-order'),
    path('api/purchase_orders/<int:po_id>/update/', update_purchase_order, name='update-purchase-order'),
    path('api/purchase_orders/<int:po_id>/delete/', delete_purchase_order, name='delete-purchase-order'),
    path('api/vendors/<int:vendor_id>/performance/',get_vendor_performance, name='get_vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', acknowledge_purchase_order,name='acknowledge_purchase_order'), 
]
