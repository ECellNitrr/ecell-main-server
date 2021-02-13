from django.http import response
from rest_framework.test import APITestCase, APIClient
from tests.AuthAPITestCase import AuthAPITestCase
from rest_framework import status

class GetUserDetailsTestCase(AuthAPITestCase):

    get_user_details_api = "/users/get_user_details/"
    
    def setUp(self):
        super(GetUserDetailsTestCase,self).setUp()

    def test_success_authorized_user(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.get_user_details_api)
        data_user = {
            'first_name': 'Crash',
            'last_name': 'Test',
            'email': self.auth_user_email,
            'verified': False,
            'contact': '+919999999999',
            'bquiz_score': 0,
            'user_type': 'GST',
            'linkedin': None,
            'facebook': None,
            'applied': False,
            'id': 2
        }
        self.assertEqual(response.data, data_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_fail_unauthorized_user(self):
        unauth_client = APIClient()
        response = unauth_client.get(self.get_user_details_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

 
class UserVerifiedTestCase(AuthAPITestCase):
    is_user_verified_api = "/users/is_user_verified/"
    
    def setUp(self):
        super(UserVerifiedTestCase,self).setUp()
    
    #Verified auth client pass 
    def test_pass_verified_user(self):
        verified_auth_client = self.create_verified_auth_client()
        response = verified_auth_client.get(self.is_user_verified_api)
        self.assertEqual(response.data['verified'],True)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Logged in user but not verified
    def test_fail_not_verified(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.is_user_verified_api)
        self.assertEqual(response.data['verified'],False)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Unauthorized user
    def test_fail_not_authorized(self):
        unauth_client = APIClient()
        response = unauth_client.get(self.is_user_verified_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


class CAApprovalTestCase(AuthAPITestCase):
    request_ca_approval_api = "/users/request_ca_approval/"
    
    def setUp(self):
        super(CAApprovalTestCase,self).setUp()

    #Auth user successful application
    def test_pass_auth_user(self):
        auth_client = self.create_auth_client()
        response = auth_client.get(self.request_ca_approval_api)
        #Successfully applied
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        #Already applied
        response = auth_client.get(self.request_ca_approval_api)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    #Unauth user test case fail
    def test_fail_unauth_user(self):
        unauth_client = APIClient()
        response = unauth_client.get(self.request_ca_approval_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
