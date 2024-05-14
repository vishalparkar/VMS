from django.urls import path
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceViewSet

schema_view = get_schema_view(title='Vendor Management API')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/vendors', VendorViewSet.as_view(), name='vendors-list'),
    path('api/vendors/<int:vendor_id>', VendorViewSet.as_view(), name='vendor-details'),
    path('api/purchase-orders', PurchaseOrderViewSet.as_view(), name='purchase-orders-list'),
    path('api/purchase-orders/<int:purchase_order_id>', PurchaseOrderViewSet.as_view(), name='purchase-order-details'),
    path('api/vendors/<int:vendor_id>/performance', HistoricalPerformanceViewSet.as_view(), name='vendor-performance'),
    path('schema/', schema_view),
]