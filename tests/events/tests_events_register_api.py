from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.models import Event
from users.models import CustomUser
from tests.AuthAPITestCase import AuthAPITestCase

class EventRegisterTestCase(AuthAPITestCase):
    def setUp(self):
        super(EventRegisterTestCase,self).setUp()
        """
        Create different events with different years and flag input in test database
        """
        
        self.event = Event.objects.create(
            id=1,
            name= "test1",
            venue = "test_venue",
            time ="test_time",
            details= "test_details",
            details_html= "test.html",
            cover_pic = "test_cover.jpeg",
            icon= "test_icon.png",
            email= "test@email.com",
            flag = True,
            year = 2019,
        )

    def test_fail_invalid_endpoint(self):
        """
        Test with invalid endpoint
        """ 
        post_register_event_api = "/events/register/twentieth/"
        verified_auth_client = self.create_verified_auth_client()
        response = verified_auth_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_fail_unauthenticated_user(self):
        """
        Test with unauthenticated user
        """
        post_register_event_api = "/events/register/1/"
        get_client = APIClient()
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_fail_unverified_user(self):
        """
        Test with unverified user
        """  
        post_register_event_api = "/events/register/1/"
        get_client = self.create_auth_client()
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_pass_registeration(self):    
        """
        Test with registeration
        """
        post_register_event_api = "/events/register/1/"
        verified_auth_client = self.create_verified_auth_client()
        response = verified_auth_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_fail_event_not_found(self):    
        """
        Test with event not found
        """
        post_register_event_api = "/events/register/12345/"
        verified_auth_client = self.create_verified_auth_client()
        response = verified_auth_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND) 

    def test_pass_re_registeration(self):
        """
        Test with re-registeration
        """       
        post_register_event_api = "/events/register/1/"
        verified_auth_client = self.create_verified_auth_client()
        response_registeration = verified_auth_client.post(post_register_event_api)
        response_re_registeration = verified_auth_client.post(post_register_event_api)
        self.assertEqual(response_re_registeration.status_code,status.HTTP_200_OK)

    def tearDown(self):
        self.event.delete()
