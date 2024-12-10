from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from .serializers import *
from .models import *

# Create your tests here.


class LoginUserTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="joel", password="joel")
        user = User.objects.get(username="joel")
        user.set_password("joel")
        user.save()
        # token = Token.objects.create(user=user)

    def test_login_user(self):
        url = reverse("token_obtain_pair")
        data = {"username": "joel", "password": "joel"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_logout_user(self):
    #     token_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzYzOTg0LCJpYXQiOjE3MzM3NjM2ODQsImp0aSI6IjZkNjRmZTRjMGE5YjRhZTRhN2QxNWJkM2ZhODM1MWFjIiwidXNlcl9pZCI6M30.pt2idC0vOY4jWYatY34oXOc2DmWO9eGe8bFWmbm19YQ"
    #     self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token_key)
    #     response = self.client.get(reverse("basic_logout"))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateUserTests(APITestCase):

    def test_create_account(self):

        url = reverse("add_student")
        data = {"username": "ajika", "password": "t1"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CreateResidentTests(APITestCase):

    def test_create_country(self):

        url = reverse("add_resident")
        data = {"name": "Resident-1", "size": 1}
        # token_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMzNzYzOTg0LCJpYXQiOjE3MzM3NjM2ODQsImp0aSI6IjZkNjRmZTRjMGE5YjRhZTRhN2QxNWJkM2ZhODM1MWFjIiwidXNlcl9pZCI6M30.pt2idC0vOY4jWYatY34oXOc2DmWO9eGe8bFWmbm19YQ"
        # self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token_key)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListResidentTests(APITestCase):

    def test_view_country(self):

        url = reverse("view_residents")
        data = Resident.objects.all()
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FilterResidentTests(APITestCase):

    def test_filter_country(self):

        url = reverse("view_residents")
        data = {"name": "a"}
        response = self.client.get(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
