from users.models import CustomUser
from rest_framework.test import APITestCase
from rest_framework import status

class ForgetPasswordTestCase(APITestCase):

    forget_password_api = '/users/forgot_password/'

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

    
    def test_fail_invalid_email(self):
        invalid_email_data = {
            'email' : 'invalid.email.com'
        }
        response = self.client.post(self.forget_password_api, invalid_email_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_fail_unregistered_email(self):
        unregistered_email_data = {
            'email' :'user@example.com'
        }
        response = self.client.post(self.forget_password_api, unregistered_email_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_success_valid_email(self):
        valid_email_data = {
            'email' :'crash.test.dummy@gmail.com'
        }
        response = self.client.post(self.forget_password_api, valid_email_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def tearDown(self):
        self.user.delete()