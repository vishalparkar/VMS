from rest_framework import generics
from rest_framework.permissions import IsAuthenticated  # Permission for authenticated users only
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .models import Vendor, PurchaseOrder, HistoricalPerformance, UserProfile
from .serializers import VendorSerializer, PurchaseOrderSerializer, UserProfileSerializer

class VendorViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all operations

class PurchaseOrderViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all operations

    def perform_create(self, serializer):
        # Override to set the owner of the purchase order to the authenticated user
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given vendor,
        by filtering against a `vendor_id` query parameter in the URL.
        """
        queryset = super().get_queryset()
        vendor_id = self.request.query_params.get('vendor_id')
        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

class HistoricalPerformanceViewSet(generics.ListAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all operations

    # Filter by vendor as there may be multiple historical performance records per vendor
    filter_backends = [DjangoFilterBackend]  # Enable filtering based on vendor
    filterset_fields = ['vendor']
    ordering_fields = ['date']
    ordering = ['-date']
    pagination_class = PageNumberPagination
    page_size = 10    

class UserProfileViewSet(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for all operations
