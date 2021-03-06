from rest_framework.test import APITestCase
from rest_framework import status
from users.models import CustomUser
from rest_framework.authtoken.models import Token


class LoginTestCase(APITestCase):

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


    def tearDown(self):
        self.user.delete()


    def test_login_success_with_correct_credentials(self):
        data = {
            "email" : self.email,
            "password" : self.password
        }
        response = self.client.post("/users/login/", data)

        # check successful login
        self.assertEqual(response.status_code , status.HTTP_202_ACCEPTED)


        # check the token recieved with /core/check_auth/ API
        self.client.credentials(HTTP_AUTHORIZATION=response.data['token'])
        response = self.client.get('/core/check_auth/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # unset the set headers
        self.client.credentials()


    def test_error_no_input(self):
        response = self.client.post("/users/login/", {})
        
        # check successful login
        self.assertEqual(response.status_code , status.HTTP_400_BAD_REQUEST)


    def test_error_wrong_credentials(self):
        data = {
            "email" : self.email,
            "password" : 'wrong password'
        }
        response = self.client.post("/users/login/", data)
        
        # check successful login
        self.assertEqual(response.status_code , status.HTTP_401_UNAUTHORIZED)

    def test_error_unregistered_email(self):
        data = {
            "email" : 'unregistereduser@email.com',
            "password" : 'any password'
        }
        response = self.client.post("/users/login/", data)

        # check successful login
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
