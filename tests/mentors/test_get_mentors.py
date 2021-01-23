from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from mentors.models import Mentor


class MentorsListTestCase(APITestCase):
    def setUp(self):
        """
        Create different mentors with different years and flag input in test database
        """
        self.mentor1 = Mentor.objects.create(
            id=1,
            name="test1",
            email="test@tmail.com",
            contact="0000000000",
            detail="test_detail",
            description="test_desc",
            year=2019,
            flag=True,
        )
        self.mentor2 = Mentor.objects.create(
            id=2,
            name='test2',
            email="test2@tmail.com",
            contact="1111111111",
            detail="test_detail",
            description="test_desc",
            year=2019,
            flag=True,
        )
        self.mentor3 = Mentor.objects.create(
            id=3,
            name='test3',
            email="test3@tmail.com",
            contact="2222222222",
            detail="test_detail",
            description="test_desc",
            year=2019,
            flag=False,
        )
        self.mentor4 = Mentor.objects.create(
            id=4,
            name='test4',
            email="test4@tmail.com",
            contact="3333333333",
            detail="test_detail",
            description="test_desc",
            year=2020,
            flag=True,
        )

    def test_pass_get_mentors_many(self):
        """
        Test for mulitple mentors
        """
        get_group_api = "/mentors/list/2019/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)

    def test_pass_get_mentors_single(self):
        """
        Test for single mentor
        """
        get_group_api = "/mentors/list/2020/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 1)

    def test_pass_get_mentors_empty(self):
        """
        Test with no mentors for a particular year
        """
        get_group_api = "/mentors/list/2021/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 0)

    def test_fail_invalid_input(self):
        """
        Test with invalid input
        """
        get_group_api = "/mentors/list/twentieth/"
        get_client = APIClient()
        response = get_client.get(get_group_api)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def tearDown(self):
        self.mentor1.delete()
        self.mentor2.delete()
        self.mentor3.delete()
        self.mentor4.delete()
