# vendors/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from vendors.models import Vendor, VendorOrder, VendorOrderItem, VendorProduct
from inventory.models import Inventory
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
        
        # Create a vendor product
        self.vendor_product = VendorProduct.objects.create(
            name='Test Product',
            vendor=self.vendor,
            description='Test Description',
            price=Decimal('12.00')
        )
        
        # Create a vendor order
        self.vendor_order = VendorOrder.objects.create(
            vendor=self.vendor,  # Ensure the vendor field is set
            status='pending',
            freight_price=Decimal('10.00'),
            created_by=self.user,
            updated_by=self.user
        )
        
        # Create vendor order items
        self.vendor_order_item = VendorOrderItem.objects.create(
            order=self.vendor_order,
            product=self.vendor_product.name,
            price=Decimal('12.00'),
            quantity=5
        )

    def test_inventory_update_on_delivery(self):
        # Change the status to 'delivered'
        self.vendor_order.status = 'delivered'
        self.vendor_order.save()

        # Fetch the updated inventory item
        inventory_item = Inventory.objects.get(product=self.vendor_product.name)

        # Check if the quantity is updated correctly
        self.assertEqual(inventory_item.quantity, 5)

        # Check if the cost price is updated correctly
        expected_total_cost = Decimal('12.00') * 5  # Adjusted to use only price
        self.assertEqual(inventory_item.cost_price, expected_total_cost)

        # Check if the description is updated correctly
        expected_description = f"- Last bought from Test Vendor, quantity: 5, for $12.00 each, in {self.vendor_order.created_at}\nProduct - Test Description"
        self.assertIn(expected_description, inventory_item.description)