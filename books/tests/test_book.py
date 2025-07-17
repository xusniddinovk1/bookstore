from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser
from books.models import Book, Author, Category
from comments.models import Comment


class BookViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='+998901234567', username='user', email='user@mail.com', password='testpass')
        self.admin = CustomUser.objects.create_user(
            phone_number='+998901234568', username='admin', email='admin@mail.com', password='adminpass', is_staff=True)

        self.category = Category.objects.create(name='Tech')
        self.author = Author.objects.create(name='John Doe', bio='Developer')
        self.book = Book.objects.create(
            title='Python 101',
            description='Learn Python',
            price=100000,
            stock=10,
            category=self.category,
            author=self.author
        )
        Comment.objects.create(user=self.user, book=self.book, rating=4, text='Good!')
        Comment.objects.create(user=self.admin, book=self.book, rating=5, text='Excellent!')

    def test_list_books(self):
        self.client.force_authenticate(self.user)
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)

    def test_avg_rating(self):
        self.client.force_authenticate(self.user)
        url = reverse('book-avg-rating', args=[self.book.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_rating'], 4.5)

    def test_top_rated(self):
        self.client.force_authenticate(self.user)
        url = reverse('book-top-rated')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], 'Python 101')

    def test_create_book_permission_denied(self):
        self.client.force_authenticate(self.user)
        url = reverse('book-list')
        data = {
            "title": "Django Book",
            "description": "Backend development",
            "price": 50000,
            "stock": 5,
            "category": self.category.id,
            "author": self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_book_by_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse('book-list')
        data = {
            "title": "Django Book",
            "description": "Backend development",
            "price": 50000,
            "stock": 5,
            "category": self.category.id,
            "author": self.author.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
