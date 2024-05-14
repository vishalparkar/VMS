from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer

def test_create_vendor(self):
    url = reverse('vendors-list')
    data = {'name': 'Test Vendor'}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Vendor.objects.count(), 1)
    self.assertEqual(response.data['name'], data['name'])

def test_get_all_vendors(self):
    vendor1 = Vendor.objects.create(name='Vendor 1')
    vendor2 = Vendor.objects.create(name='Vendor 2')
    url = reverse('vendors-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    serializer = VendorSerializer([vendor1, vendor2], many=True)
    self.assertEqual(response.data, serializer.data)

class PurchaseOrderTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor', contact_details='Test Contact', address='Test Address', vendor_code='V123')
        self.purchase_order_data = {
            'po_number': 'PO12345',
            'vendor': self.vendor.id,
            'order_date': '2023-01-01T00:00:00Z',
            'delivery_date': '2023-01-15T00:00:00Z',
            'items': '{"item1": "10", "item2": "20"}',
            'quantity': 30,
            'status': 'pending'
        }
        self.response = self.client.post(
            reverse('purchase-orders-list'),
            self.purchase_order_data,
            format="json"
        )

    def test_create_purchase_order(self):
        """Test creating a purchase order."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 1)
        self.assertEqual(PurchaseOrder.objects.get().po_number, 'PO12345')

    def test_get_purchase_order(self):
        """Test retrieving a purchase order."""
        purchase_order = PurchaseOrder.objects.get()
        response = self.client.get(
            reverse('purchase-order-detail', kwargs={'pk': purchase_order.id}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['po_number'], 'PO12345')