from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from events.models import Event


class EventsListTestCase(APITestCase):
    def setUp(self):
        """
        Create different events with different years and flag input in test database
        """
        self.event1 = Event.objects.create(
            id=0,
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
        self.event2 = Event.objects.create(
            id=1,
            name="test2",
            venue="test_venue",
            time="test_time",
            details="test_details",
            details_html="test.html",
            cover_pic="test_cover.jpeg",
            icon="test_icon.png",
            email="test@email.com",
            flag=True,
            year=2019,
        )
        self.event3 = Event.objects.create(
            id=2,
            name="test3",
            venue="test_venue",
            time="test_time",
            details="test_details",
            details_html="test.html",
            cover_pic="test_cover.jpeg",
            icon="test_icon.png",
            email="test@email.com",
            flag=False,
            year=2019,
        )
        self.event4 = Event.objects.create(
            id=3,
            name="test4",
            venue="test_venue",
            time="test_time",
            details="test_details",
            details_html="test.html",
            cover_pic="test_cover.jpeg",
            icon="test_icon.png",
            email="test@email.com",
            flag=True,
            year=2020,
        )

    def test_pass_get_mentors_many(self):
        """
        Test for mulitple events
        """
        get_group_api = "/events/list/2019/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(len(response.data['data']), 2)

    def test_pass_get_events_single(self):
        """
        Test for single event
        """
        get_group_api = "/events/list/2020/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(len(response.data['data']), 1)

    def test_pass_get_events_empty(self):
        """
        Test with no events for a particular year
        """
        get_group_api = "/events/list/2021/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(len(response.data['data']), 0)

    def test_fail_invalid_input(self):
        """
        Test with invalid input
        """
        get_group_api = "/events/list/twentieth/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        self.event1.delete()
        self.event2.delete()
        self.event3.delete()
        self.event4.delete()
