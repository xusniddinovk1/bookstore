from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from books.models import Book, Author, Category
from orders.models import Order, OrderItem


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='+998901234567', username='user', email='user@mail.com', password='testpass')
        self.admin = CustomUser.objects.create_user(
            phone_number='+998901234568', username='admin', email='admin@mail.com', password='adminpass', is_staff=True)
        self.category = Category.objects.create(name='Fiction')
        self.author = Author.objects.create(name='Writer', bio='Bio')
        self.book = Book.objects.create(title='Book', description='Desc', price=10000, stock=10, category=self.category,
                                        author=self.author)
        self.client.force_authenticate(self.user)

    def test_create_order(self):
        url = reverse('order-list')
        data = {
            'phone_number': self.user.phone_number,
            'items': [{'book': self.book.id, 'quantity': 1}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)

    def test_pdf_export_admin_only(self):
        self.client.force_authenticate(self.admin)
        url = reverse('order-export-pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_export_permission_denied(self):
        self.client.force_authenticate(self.user)
        url = reverse('order-export-pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
