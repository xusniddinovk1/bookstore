from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import CustomUser


class AuthTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='+998901234567',
            username='user1',
            email='user1@mail.com',
            password='testpass'
        )

    def test_register(self):
        url = reverse('register')
        data = {
            "phone_number": "+998901112233",
            "username": "newuser",
            "email": "new@mail.com",
            "password": "newpass123"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_login(self):
        url = reverse('login')
        data = {
            "phone_number": "+998901234567",
            "password": "testpass"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)

    def test_logout(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self.user)
        self.client.force_authenticate(user=self.user)
        url = reverse('logout')
        response = self.client.post(url, {"refresh": str(refresh)})
        self.assertEqual(response.status_code, 205)
