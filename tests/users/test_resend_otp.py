from rest_framework.test import APIClient
from rest_framework import status
from tests.AuthAPITestCase import AuthAPITestCase

class ResendOTPTestCase(AuthAPITestCase):

    def setUp(self):
        '''
             Creating a user for resend_otp api using AuthAPITestCAse
        '''
        super(ResendOTPTestCase, self).setUp()

    def test_fail_unregistered_user(self):
        '''
             Testing with unregistered user
        '''
        unauth_client = APIClient()
        response = unauth_client.get("/users/resend_otp/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_success_registered_user(self):
        '''
            Testing with registered user
        '''
        auth_client = self.create_auth_client()
        response = auth_client.get("/users/resend_otp/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
