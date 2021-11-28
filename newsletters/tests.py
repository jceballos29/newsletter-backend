from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from newsletters.models import Tag, Newsletter


class AccountTestCase(APITestCase):

    def setUp(self) -> None:
        self.host = 'http://127.0.0.1:8000'
        self.admin = User.objects.create_user(
            username="admin_test",
            first_name="Admin",
            last_name="Test",
            email="admin_test@newsletter.com",
            password="admin@test_123",
            is_staff=True
        )

        self.admin2 = User.objects.create_user(
            username="admin2_test",
            first_name="Admin2",
            last_name="Test",
            email="admin2_test@newsletter.com",
            password="admin@test_123",
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="user_test",
            first_name="User",
            last_name="Test",
            email="user_test@newsletter.com",
            password="user@test_123",
            is_staff=False
        )

        self.tag = Tag(name="Test", slug="test")
        self.tag.save()

        self.tag_1 = Tag(name="Test 1", slug="test_1")
        self.tag_1.save()

        self.newsletter = Newsletter.objects.create(
            name="Newsletter Test",
            description="Is a test newsletter",
            image_url="http://image.t/test",
            target=1
        )
        self.newsletter.tags.add(self.tag)
        self.newsletter.created_by = self.admin
        self.newsletter.votes.add(self.user)
        self.newsletter.subscribers.add(self.user)
        self.newsletter.save()

        self.newsletter_1 = Newsletter.objects.create(
            name="Newsletter Test 1",
            description="Is a test newsletter",
            image_url="http://image.t/test",
            target=1
        )
        self.newsletter_1.tags.add(self.tag_1)
        self.newsletter_1.created_by = self.admin
        self.newsletter_1.published = True
        self.newsletter_1.save()

        response = self.client.post(
            f'{self.host}/login/',
            {"username": "admin_test", "password": "admin@test_123"})
        self.admin_token = response.data["access"]

        response = self.client.post(
            f'{self.host}/login/',
            {"username": "user_test", "password": "user@test_123"})
        self.user_token = response.data["access"]

# Admin --------------------------------------
    def test_get_list(self):
        response = self.client.get(
            f'{self.host}/newsletters/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['count'], 0)
        self.assertNotEqual(len(response.data['results']), 0)

    def test_get_list_filter(self):
        response = self.client.get(
            f'{self.host}/newsletters/?tags__slug__icontains=test',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['count'], 0)
        self.assertNotEqual(len(response.data['results']), 0)

    def test_create_newsletter(self):
        new_newsletter = {
            "name": "Customer Science in Analytics",
            "description": "A perspective on how “Small Scale Businesses” can use data to Improve Customer Retention",
            "image_url": "https://miro.medium.com/max/1400/0*5QvB5J1O0DxAHIMu",
            "tags": [1],
            "frequency": 1
        }

        response = self.client.post(
            f'{self.host}/newsletters/',
            new_newsletter,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        result = Newsletter.objects.filter(name=new_newsletter["name"])

        self.assertTrue(result.exists())
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], new_newsletter['name'])

    def test_create_publish(self):
        newsletter = Newsletter.objects.get(name="Newsletter Test")
        response = self.client.post(
            f'{self.host}/newsletters/{newsletter.id}/publish/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        result = Newsletter.objects.get(name="Newsletter Test")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(result.published)

    def test_create_share(self):
        newsletter = Newsletter.objects.get(name="Newsletter Test 1")

        response = self.client.post(
            f'{self.host}/newsletters/{newsletter.id}/share/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        self.assertEqual(response.status_code, 200)

# User ----------------------------------------
    def test_subscribe(self):
        response = self.client.post(
            f'{self.host}/newsletters/{self.newsletter_1.id}/subscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(self.user.subscriptions.all()), 0)
        self.assertTrue(self.newsletter_1 in self.user.subscriptions.all())

    def test_vote(self):
        response = self.client.post(
            f'{self.host}/newsletters/{self.newsletter_1.id}/vote/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user in self.newsletter_1.votes.all())

    def test_list_subscribed(self):
        response = self.client.get(
            f'{self.host}/newsletters/subscribed/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )
        result = self.user.subscriptions.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(result))

    def test_unsubscribe(self):
        response = self.client.post(
            f'{self.host}/newsletters/{self.newsletter.id}/unsubscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.newsletter_1 in self.user.subscriptions.all())
