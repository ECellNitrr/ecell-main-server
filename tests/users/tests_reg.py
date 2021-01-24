from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

class RegistrationTestCase(APITestCase):


    def test_registration_success_with_correct_credentials(self):
        data = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "contact": "string",
            "password": "stringstring"
            }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_login = {

            "email" : "user@example.com",
            "password": "stringstring"
        }

        response = self.client.post("/users/login/", data_login)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_registration_with_used_email(self):
        data =  {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "contact": "string",
            "password": "stringstring"
            }

        response = self.client.post("/users/register/", data)
        response = self.client.post("/users/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_registration_without_email(self):
        data =  {
            "first_name": "string",
            "last_name": "string",
            "contact": "string",
            "password": "stringstring"
            }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_without_name(self):
        data =  {
            
            "email": "user@example.com",
            "contact": "string",
            "password": "stringstring"
            }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_without_password(self):
        data =  {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "contact": "string"
            }

        response = self.client.post("/users/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_email(self):
        data =  {
            "first_name": "string",
            "last_name": "string",
            "email": "userexample.com",
            "contact": "string",
            "password": "stringstring"
            }

        response = self.client.post("/users/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_small_password(self):
        data = {
            "first_name": "string",
            "last_name": "string",
            "email": "user@example.com",
            "contact": "string",
            "password": "str"
            }

        response = self.client.post("/users/register/", data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)