from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from planetarium.models import ShowSession
from planetarium.serializers import ShowSessionListSerializer
from planetarium.tests.default_test_data import user_test, sample_show_theme, sample_astronomy_show, \
    sample_planetarium_dome, sample_show_session

Show_Session_URL = reverse("planetarium:show_session-list")


class UnauthenticatedSAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="tiguti2626")

    def test_auth_required(self):
        res = self.client.get(Show_Session_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedShowSessionApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_list_show_session(self):
        """Show session object 1"""
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)
        show_session_object = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19"
        )

        """Show session object 2"""
        astronomy_show_object_2 = sample_astronomy_show(
            title="Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='Sample Theme 2'))
        planetarium_dome_object_2 = sample_planetarium_dome(name="Planetarium Dome Test2", rows=45, seats_in_row=250)
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_2,
            planetarium_dome=planetarium_dome_object_2,
            show_time="2024-06-19"
        )

        res = self.client.get(Show_Session_URL)
        show_session_show = ShowSession.objects.all()
        serializer = ShowSessionListSerializer(show_session_show, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_create_show_session(self):
        """Show session object 1"""
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)

        payload = {
            "astronomy_show": astronomy_show_object,
            "planetarium_dome": planetarium_dome_object,
            "show_time": "2024-06-20"
        }
        res = self.client.post(Show_Session_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_create_show_session(self):
        test_user = user_test(username="admin", password="testadmin26", is_staff=True)
        self.client.force_authenticate(test_user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)

        payload = {
            "astronomy_show": astronomy_show_object.id,
            "planetarium_dome": planetarium_dome_object.id,
            "show_time": "2024-06-18"
        }
        res = self.client.post(Show_Session_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class ShowSessionFilteringApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_filter_show_session_show_name(self):
        """Show session object 1"""
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19"
        )

        """Show session object 2"""
        astronomy_show_object_2 = sample_astronomy_show(
            title="new Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='new Sample Theme 2'))
        planetarium_dome_object_2 = sample_planetarium_dome(name="Planetarium Dome Test2", rows=45, seats_in_row=250)
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_2,
            planetarium_dome=planetarium_dome_object_2,
            show_time="2024-06-19"
        )
        """Show session object 3"""
        astronomy_show_object_3 = sample_astronomy_show(
            title="No Match",
            description="New description 3",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name='Sample Theme 3'))
        planetarium_dome_object_3 = sample_planetarium_dome(name="Planetarium Dome Test3", rows=45, seats_in_row=250)
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_3,
            planetarium_dome=planetarium_dome_object_3,
            show_time="2024-06-20"
        )
        res = self.client.get(Show_Session_URL, {"show_name": "new"})
        serializer1 = ShowSessionListSerializer(show_session_object_1)
        serializer2 = ShowSessionListSerializer(show_session_object_2)
        serializer3 = ShowSessionListSerializer(show_session_object_3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_show_session_astronomy_description(self):
        """Show session object 1"""
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19"
        )

        """Show session object 2"""
        astronomy_show_object_2 = sample_astronomy_show(
            title="new Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='new Sample Theme 2'))
        planetarium_dome_object_2 = sample_planetarium_dome(name="Planetarium Dome Test2", rows=45, seats_in_row=250)
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_2,
            planetarium_dome=planetarium_dome_object_2,
            show_time="2024-06-19"
        )
        """Show session object 3"""
        astronomy_show_object_3 = sample_astronomy_show(
            title="New Astronomy Show 3",
            description="No Match",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name='Sample Theme 3'))
        planetarium_dome_object_3 = sample_planetarium_dome(name="Planetarium Dome Test3", rows=45, seats_in_row=250)
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_3,
            planetarium_dome=planetarium_dome_object_3,
            show_time="2024-06-20"
        )
        res = self.client.get(Show_Session_URL, {"description": "new"})
        serializer1 = ShowSessionListSerializer(show_session_object_1)
        serializer2 = ShowSessionListSerializer(show_session_object_2)
        serializer3 = ShowSessionListSerializer(show_session_object_3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_show_session_astronomy_planetarium_dome_name(self):
        """Show session object 1"""
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19"
        )

        """Show session object 2"""
        astronomy_show_object_2 = sample_astronomy_show(
            title="new Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='new Sample Theme 2'))
        planetarium_dome_object_2 = sample_planetarium_dome(name="Planetarium Dome Test2", rows=45, seats_in_row=250)
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_2,
            planetarium_dome=planetarium_dome_object_2,
            show_time="2024-06-19"
        )
        """Show session object 3"""
        astronomy_show_object_3 = sample_astronomy_show(
            title="New Astronomy Show 3",
            description="description3",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name='Sample Theme 3'))
        planetarium_dome_object_3 = sample_planetarium_dome(name="No Match", rows=45, seats_in_row=250)
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_3,
            planetarium_dome=planetarium_dome_object_3,
            show_time="2024-06-20"
        )
        res = self.client.get(Show_Session_URL, {"name": "Planetarium"})
        serializer1 = ShowSessionListSerializer(show_session_object_1)
        serializer2 = ShowSessionListSerializer(show_session_object_2)
        serializer3 = ShowSessionListSerializer(show_session_object_3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_show_session_show_time(self):
        """Show session object 1"""
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19"
        )

        """Show session object 2"""
        astronomy_show_object_2 = sample_astronomy_show(
            title="new Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='new Sample Theme 2'))
        planetarium_dome_object_2 = sample_planetarium_dome(name="Planetarium Dome Test2", rows=45, seats_in_row=250)
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_2,
            planetarium_dome=planetarium_dome_object_2,
            show_time="2024-06-19"
        )
        """Show session object 3"""
        astronomy_show_object_3 = sample_astronomy_show(
            title="New Astronomy Show 3",
            description="description3",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name='Sample Theme 3'))
        planetarium_dome_object_3 = sample_planetarium_dome(name="No Match", rows=45, seats_in_row=250)
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object_3,
            planetarium_dome=planetarium_dome_object_3,
            show_time="2024-06-20"
        )
        res1 = self.client.get(Show_Session_URL, {"show_time": "2024-05-19"})
        res2 = self.client.get(Show_Session_URL, {"show_time": "2024-06-19"})
        res3 = self.client.get(Show_Session_URL, {"show_time": "2024-09-19"})
        serializer1 = ShowSessionListSerializer(show_session_object_1)
        serializer2 = ShowSessionListSerializer(show_session_object_2)
        serializer3 = ShowSessionListSerializer(show_session_object_3)
        self.assertIn(serializer1.data, res1.data)
        self.assertIn(serializer2.data, res2.data)
        self.assertNotIn(serializer3.data, res3.data)


class ShowSessionModelsTestsStr(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_show_theme_str(self):
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(name="Planetarium Dome Test1", rows=40, seats_in_row=200)
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19"
        )

        self.assertEqual(show_session_object_1.__str__(),
                         (f"Show session name: {show_session_object_1.astronomy_show.title} ,"
                          f" planetarium: {show_session_object_1.planetarium_dome.name} , show time: {show_session_object_1.show_time}"))
