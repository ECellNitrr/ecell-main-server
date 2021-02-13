from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from users.models import CustomUser


class ResendOTPTestCase(APITestCase):
    '''
        Creating a user for resend_otp api
    '''
    def setUp(self):
        self.email = "test@gmail.com"
        self.password = "password"

        self.user = CustomUser.objects.create_user(
            email = self.email,
            username = self.email,
            first_name = "well",
            last_name = "done",
            contact = "+919999999999",
            password = self.password,
            verified = False,
        )

    '''
        Creating an auth client
    '''
    def create_auth_client(self):
        login_api = "/users/login/"
        login_payload = {
            "email": self.email,
            "password": self.password
        }
        auth_client = APIClient()
        login_response = auth_client.post(login_api, login_payload)
        auth_token = login_response.data['token']
        auth_client.credentials(HTTP_AUTHORIZATION=auth_token)
        return auth_client

    '''
        Testing with unregistered user
    '''
    def test_fail_unregistered_user(self):
        unauth_client = APIClient()
        response = unauth_client.get("/users/resend_otp/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    '''
        Testing with registered user
    '''
    def test_success_registered_user(self):
        auth_client = self.create_auth_client()
        response = auth_client.get("/users/resend_otp/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()
