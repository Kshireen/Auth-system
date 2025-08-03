from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserAuthTests(APITestCase):

    def test_register_user_success(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post("/api/register/", data)  # change path if different
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_missing_fields(self):
        data = {
            "username": "useronly"
            # missing email and password
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_duplicate(self):
        User.objects.create_user(username="existing", email="exist@example.com", password="pass123")
        data = {
            "username": "existing",
            "email": "exist@example.com",
            "password": "pass123"
        }
        response = self.client.post("/api/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        User.objects.create_user(username="loginuser", password="loginpass")
        data = {
            "username": "loginuser",
            "password": "loginpass"
        }
        response = self.client.post("/api/login/", data)  # change if URL is different
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_failure(self):
        User.objects.create_user(username="wronguser", password="rightpass")
        data = {
            "username": "wronguser",
            "password": "wrongpass"
        }
        response = self.client.post("/api/login/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
