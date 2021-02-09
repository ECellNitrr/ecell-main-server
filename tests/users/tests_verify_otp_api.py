from users.models import CustomUser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class VerifyOTPTestCase(APITestCase):

    verify_otp_api = '/users/verify_otp/'

    def setUp(self):
        self.email = "crash.test.dummy@gmail.com"
        self.password = "test.modelx"

        self.user = CustomUser.objects.create_user(
            email = self.email,
            username = self.email,
            first_name = "Crash",
            last_name = "Test",
            contact = "+919999999999",
            password = self.password,
            otp = "1234"
        )

    def create_auth_client(self):
        login_api = "/users/login/"
        login_payload = {
            'email': self.email,
            'password': self.password
        }

        auth_client = APIClient()
        login_response = auth_client.post(login_api, login_payload)
        auth_token = login_response.data['token']
        auth_client.credentials(HTTP_AUTHORIZATION=auth_token)
        return auth_client

    #Unauth user test fail
    def test_fail_unauth_user(self):
        unauth_client = APIClient()
        data = {
            "otp" : self.user.otp
        }
        response = unauth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    #Test fail with no otp
    def test_fail_auth_no_otp(self):
        auth_client = self.create_auth_client()
        data = {}
        response = auth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    #Test fail with wrong otp
    def test_fail_auth_wrong_otp(self):
        auth_client = self.create_auth_client()
        data = {
            "otp" : "4321"
        }
        response = auth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    #Test pass with correct OTP
    def test_pass_correct_otp(self):
        auth_client = self.create_auth_client()
        data = {
            "otp" : self.user.otp
        }
        response = auth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Test fail with already verified otp
    def test_fail_already_verified(self):
        auth_client = self.create_auth_client()
        data = {
            "otp" : self.user.otp
        }
        response = auth_client.post(self.verify_otp_api,data)
        response = auth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.user.delete()