# vendors/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from vendors.models import Vendor, VendorOrder, VendorOrderItem
from decimal import Decimal

class VendorOrderTests(TestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # Create a vendor
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            address='123 Test St',
            phone='1234567890',
            email='test@example.com',
            contact='Test Contact',
            created_by=self.user,
            updated_by=self.user
        )
        
        # Create a vendor order
        self.order = VendorOrder.objects.create(
            vendor=self.vendor,  # Ensure the vendor field is set
            status='pending',
            freight_price=Decimal('10.00'),
            created_by=self.user,
            updated_by=self.user
        )
        
        # Create vendor order items
        self.item1 = VendorOrderItem.objects.create(
            order=self.order,
            product='Product 1',
            price=Decimal('20.00'),
            quantity=2
        )
        
        self.item2 = VendorOrderItem.objects.create(
            order=self.order,
            product='Product 2',
            price=Decimal('30.00'),
            quantity=1
        )

    def test_calculate_total_value(self):
        self.order.calculate_total_value()
        self.assertEqual(self.order.total_value, Decimal('70.00'))

    def test_price_with_freight(self):
        self.item1.save()
        self.item2.save()
        self.assertAlmostEqual(self.item1.priceWithFreight, Decimal('25.00'), places=2)
        self.assertAlmostEqual(self.item2.priceWithFreight, Decimal('40.00'), places=2)

    def test_order_total_value_with_freight(self):
        self.order.calculate_total_value()
        self.assertEqual(self.order.total_value_plus_freight, Decimal('80.00'))

    def test_delete_order_item(self):
        self.item1.delete()
        self.order.calculate_total_value()
        self.assertEqual(self.order.total_value, Decimal('30.00'))