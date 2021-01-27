from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class UserRegisterTestCase(APITestCase):
    def test_success_with_correct_credentials(self):
        data={
            "first_name": "string1",
            "last_name": "string2",
            "email": "user234@example.com",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_fail_with_used_email(self):
        data = {
            "first_name": "string1",
            "last_name": "string2",
            "email": "user234@example.com",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_without_fields(self):
        data = {
            "first_name": "string1",
            "email": "user1@example.com",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_incorret_email(self):
        data = {
            "first_name": "string1",
            "last_name":"str2",
            "email": "user1_example_com",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_without_email(self):
        data = {
            "first_name": "string1",
            "last_name": "str2",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_without_password(self):
        data = {
            "first_name": "string1",
            "last_name": "str2",
            "email": "user2@example.com",
            "contact": "string9000",
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_small_password(self):
        data = {
            "first_name": "string1",
            "last_name": "str2",
            "email": "user2@example.com",
            "contact": "string9000",
            "password": "str",
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_without_firstname(self):
        data = {
            "last_name": "str2",
            "email": "user2@example.com",
            "contact": "string9000",
            "password": "string989",
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_without_contact(self):
        data = {
            "first_name": "string1",
            "last_name": "str2",
            "email": "user2@example.com",
            "password": "string989",
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_blank_name(self):
        data = {
            "first_name": "",
            "last_name": "string2",
            "email": "user234@example.com",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_blank_contact(self):
        data = {
            "first_name": "string22",
            "last_name": "string2",
            "email": "user234@example.com",
            "contact": "",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_with_blank_email(self):
        data = {
            "first_name": "string1",
            "last_name": "string2",
            "email": "",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_blank_password(self):
        data = {
            "first_name": "string1",
            "last_name": "string2",
            "email": "user234@example.com",
            "contact": "string9000",
            "password": ""
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_blank_lastname(self):
        data = {
            "first_name": "string1",
            "last_name": "",
            "email": "user234@example.com",
            "contact": "string9000",
            "password": "string989"
        }

        response = self.client.post("/users/register/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
