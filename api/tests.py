from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Vendor
from .serializers import VendorSerializer

class VendorListCreateViewTest(APITestCase):

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
