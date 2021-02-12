from users.models import CustomUser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tests.AuthAPITestCase import AuthAPITestCase

class VerifyOTPTestCase(AuthAPITestCase):

    verify_otp_api = '/users/verify_otp/'

    def setUp(self):
        super(VerifyOTPTestCase,self).setUp()

    #Unauth user test fail
    def test_fail_unauth_user(self):
        unauth_client = APIClient()
        data = {
            "otp" : self.auth_user.otp
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
            "otp" : self.auth_user.otp
        }
        response = auth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Test fail with already verified otp
    def test_fail_already_verified(self):
        auth_client = self.create_auth_client()
        data = {
            "otp" : self.auth_user.otp
        }
        response = auth_client.post(self.verify_otp_api,data)
        
        # Trying to Verify again
        response = auth_client.post(self.verify_otp_api,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
