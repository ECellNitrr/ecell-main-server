from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.models import Event,EventRegister
from users.models import CustomUser

class EventRegisterTestCase(APITestCase):
    def setUp(self):
        """
        Create different events with different years and flag input in test database
        """
        self.registered_event = EventRegister.objects.create(
            id=1,
            user=1,
            event=1
        )

        self.user1= CustomUser.objects.create(
            id=0,
            email="test@email.com",
            username="test1",
            verified=False
        )

        self.user2= CustomUser.objects.create(
            id=1,
            email="test2@email.com",
            username="test2",
            verified=True
        )

        self.event1 = Event.objects.create(
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

    def test_pass_invalid_input(self):
        """
        Test with invalid input
        """ 
        post_register_event_api = "/events/register/twentieth/"
        get_client = APIClient()
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_pass_unauthorized_user(self):
        """
        Test with unauthroized user
        """
        post_register_event_api = "/events/register/0/"
        get_client = APIClient()
        response = get_client.post(post_register_event_api)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_pass_unverified_user(self):
        """
        Test with unverified user
        """  
        post_register_event_api = "/events/register/0/"
        get_client = APIClient()
        user = {'id':0,'email':'test1@email.com','username':'test1','verified':False}
        response = get_client.post(post_register_event_api,user,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_pass_reregisteration(self):    
        """
        Test with reregisteration
        """
        post_register_event_api = "/events/register/1/"
        get_client = APIClient()
        user = {'id':1,'email':'test2@email.com','username':'test2','verified':True}
        response = get_client.post(post_register_event_api,user,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def tearDown(self):
        self.registered_event.delete()
        self.user1.delete()
        self.user2.delete()
        self.event1.delete()