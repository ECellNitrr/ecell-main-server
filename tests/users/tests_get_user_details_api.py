from django.http import response
from users.models import CustomUser
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class GetUserDetailsTestCase(APITestCase):

    get_user_details_api = "/users/get_user_details/"
    
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

    def test_success_authorized_user(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.get_user_details_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_fail_unauthorized_user(self):
        unauth_client = APIClient()
        response = unauth_client.get(self.get_user_details_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.user.delete()

class UserVerifiedTestCase(APITestCase):
    is_user_verified_api = "/users/is_user_verified/"
    
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
            otp = "123456"
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

    def create_verified_auth_client(self):
        verify_otp_api = "/users/verify_otp/"
        auth_client = self.create_auth_client()
        data = {
            "otp" : self.user.otp
        }
        response = auth_client.post(verify_otp_api,data)
        return auth_client
    
    #Verified auth client pass 
    def test_pass_verified_user(self):
        verified_auth_client = self.create_verified_auth_client()
        response = verified_auth_client.get(self.is_user_verified_api)
        self.assertEqual(response.data['verified'],True)

    #Logged in user but not verified
    def test_fail_not_verified(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.is_user_verified_api)
        self.assertEqual(response.data['verified'],False)

    #Unauthorized user
    def test_fail_not_authorized(self):
        unauth_client = APIClient()
        response = unauth_client.get(self.is_user_verified_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.user.delete()

class CAApprovalTestCase(APITestCase):
    request_ca_approval_api = "/users/request_ca_approval/"
    
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

    #Auth user successful approval
    def test_pass_auth_user(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.request_ca_approval_api)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Unauth user test case fail
    def test_fail_unauth_user(self):
        unauth_client = APIClient()
        response = unauth_client.get(self.request_ca_approval_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
