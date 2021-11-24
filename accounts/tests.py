from django.contrib.auth.models import User
from rest_framework.test import APITestCase


class AccountTestCase(APITestCase):

    def setUp(self) -> None:
        self.host = 'http://127.0.0.1:8000'
        self.superuser = User.objects.create_superuser(
            username="super_test",
            email="super_test@newsletter.com",
            password="super@test_123"
        )

    def test_register_user(self):
        new_user = {
            "username": "test",
            "first_name": "test",
            "last_name": "tester",
            "email": "test@newsletter.com",
            "password": "test@123"
        }

        response = self.client.post(f'{self.host}/register/', new_user)
        result = User.objects.filter(username=new_user['username'])

        self.assertTrue(result.exists())
        self.assertEqual(result[0].username, new_user['username'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], new_user['username'])
        self.assertEqual(response.data['id'], result[0].id)

    def test_login(self):
        response = self.client.post(f'{self.host}/login/', {"username": "super_test", "password": "super@test_123"})
        self.assertContains(response, 'access', status_code=200)
