from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from books.models import Book, Author, Category
from orders.models import Order, OrderItem
from comments.models import Comment


class CommentViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='+998901234567', username='user', email='user@mail.com', password='testpass')
        self.category = Category.objects.create(name='Science')
        self.author = Author.objects.create(name='Albert', bio='Physicist')
        self.book = Book.objects.create(title='Relativity', description='Physics book', author=self.author,
                                        category=self.category, price=200000, stock=10)
        self.order = Order.objects.create(user=self.user, phone_number=self.user.phone_number, is_paid=True)
        self.item = OrderItem.objects.create(order=self.order, book=self.book, quantity=1)
        self.client.force_authenticate(self.user)

    def test_create_comment_success(self):
        url = reverse('comment-list')
        data = {
            'book': self.book.id,
            'text': 'Great book!',
            'rating': 5
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_comment_fail_if_not_bought(self):
        new_book = Book.objects.create(title='New Book', description='No buy', author=self.author,
                                       category=self.category, price=100000)
        url = reverse('comment-list')
        data = {
            'book': new_book.id,
            'text': 'I did not buy this',
            'rating': 1
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
