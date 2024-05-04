from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.exceptions import ValidationError

from planetarium.models import AstronomyShow
from planetarium.serializers import AstronomyShowListSerializer, AstronomyShowCreateSerializer
from planetarium.tests.default_test_data import user_test, sample_show_theme, sample_astronomy_show

Astronomy_Show_URL = reverse("planetarium:astronomy_show-list")


class UnauthenticatedSAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="tiguti2626")

    def test_auth_required(self):
        res = self.client.get(Astronomy_Show_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAstronomyShowApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_list_astronomy_show(self):
        obj1 = sample_astronomy_show(title="dddd", description="dwdswd")
        obj1.show_theme.add(sample_show_theme(name="Teste Theme1"))
        obj2 = sample_astronomy_show(title="dffddd", description="dwdswffd")
        obj2.show_theme.add(sample_show_theme(name="Teste Theme2"))
        res = self.client.get(Astronomy_Show_URL)
        astronomy_show = AstronomyShow.objects.all()
        serializer = AstronomyShowListSerializer(astronomy_show, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_create_astronomy_show(self):
        payload = {
            "name": "Astronomy Show Test"
        }
        res = self.client.post(Astronomy_Show_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_show_theme(self):
        test_user = user_test(username="admin", password="testadmin26", is_staff=True)
        self.client.force_authenticate(test_user)
        theme_obj = sample_show_theme(name="Sample Theme")
        payload = {
            "title": "New Astronomy Show Test",
            "description": "test description",
            "show_theme": theme_obj.id
        }
        res = self.client.post(Astronomy_Show_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AstronomyShowFilteringApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_filter_astronomy_show_title(self):
        astronomy_show_object_1 = sample_astronomy_show()
        astronomy_show_object_1.show_theme.add(sample_show_theme(name='Sample Theme 1'))
        astronomy_show_object_2 = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='Sample Theme 2'))
        astronomy_show_object_3 = sample_astronomy_show(
            title="New Astronomy Show 1",
            description="New description 1",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name="Sample Theme 3"))
        res = self.client.get(Astronomy_Show_URL, {"show_name": "new"})
        serializer3 = AstronomyShowListSerializer(astronomy_show_object_1)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_astronomy_show_show_theme(self):
        astronomy_show_object_1 = sample_astronomy_show()
        astronomy_show_object_1.show_theme.add(sample_show_theme(name='Sample Theme 1 '))
        astronomy_show_object_2 = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='Sample Theme 2'))
        astronomy_show_object_3 = sample_astronomy_show(
            title="New Astronomy Show 1",
            description="New description 1",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name="No Match"))
        res = self.client.get(Astronomy_Show_URL, {"show_theme": "sample"})
        serializer1 = AstronomyShowListSerializer(astronomy_show_object_1)
        self.assertIn(serializer1.data, res.data)
        serializer2 = AstronomyShowListSerializer(astronomy_show_object_1)
        self.assertIn(serializer2.data, res.data)
        serializer3 = AstronomyShowListSerializer(astronomy_show_object_3)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_astronomy_show_description(self):
        astronomy_show_object_1 = sample_astronomy_show()
        astronomy_show_object_1.show_theme.add(sample_show_theme(name='Sample Theme 1'))
        astronomy_show_object_2 = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object_2.show_theme.add(sample_show_theme(name='Sample Theme 2'))
        astronomy_show_object_3 = sample_astronomy_show(
            title="New Astronomy Show 1",
            description="No Match",
        )
        astronomy_show_object_3.show_theme.add(sample_show_theme(name="Sample Theme 3"))
        res = self.client.get(Astronomy_Show_URL, {"description": "desc"})
        serializer1 = AstronomyShowListSerializer(astronomy_show_object_1)
        self.assertIn(serializer1.data, res.data)
        serializer2 = AstronomyShowListSerializer(astronomy_show_object_2)
        self.assertIn(serializer2.data, res.data)
        serializer3 = AstronomyShowListSerializer(astronomy_show_object_3)
        self.assertNotIn(serializer3.data, res.data)


class AstronomyShowValidation(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_validate_astronomy_show_name_models(self):
        with self.assertRaises(IntegrityError):
            astronomy_show_object_2 = sample_astronomy_show(
                title="New Astronomy Show",
                description="New description",
            )
            astronomy_show_object_2.show_theme.add(sample_show_theme(name='Sample Theme'))
            astronomy_show_object_3 = sample_astronomy_show(
                title="New Astronomy Show 1",
                description="New description 1",
            )
            astronomy_show_object_3.show_theme.add(sample_show_theme(name="Sample Theme"))

    def test_validate_astronomy_show_name_serializer(self):
        with self.assertRaises(ValidationError):
            show_theme_object = sample_show_theme()
            payload = {"title": "New Astronomy", "description": "New description",
                       "show_theme": [show_theme_object.id, ]}
            serializer = AstronomyShowCreateSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            show_theme_object_1 = sample_show_theme(name="Test1")
            payload = {"title": "New Astronomy", "description": "New description1",
                       "show_theme": [show_theme_object_1.id, ]}
            serializer = AstronomyShowCreateSerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()


class ShowThemeModelsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="defaultpassword122")
        self.client.force_authenticate(self.user)

    def test_show_theme_str(self):
        astronomy_show_object_1 = sample_astronomy_show()
        self.assertEqual(astronomy_show_object_1.title.__str__(), "Sample Astronomy Show")
        self.assertEqual(astronomy_show_object_1.__str__(),
                         f"name_show : {astronomy_show_object_1.title} , description : {astronomy_show_object_1.description} , show_theme : {astronomy_show_object_1.show_themes}")
