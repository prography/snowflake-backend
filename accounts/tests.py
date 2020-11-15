from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(email="1@1.com", password="123")

    def test_create_user(self):
        url = reverse("accounts:user-list")
        data = {
            "email": "2@2.com",
            "password1": "123",
            "password2": "123",
            "username": "남바완",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_unique_username(self):
        url = reverse("accounts:user-list")
        data = {
            "email": "1@1.com",
            "password1": "123",
            "password2": "123",
            "username": "남2바완",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        url = reverse("accounts:user-detail", kwargs={"pk": 1})
        data = {"email": "1@2.com"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=1).email, "1@2.com")
