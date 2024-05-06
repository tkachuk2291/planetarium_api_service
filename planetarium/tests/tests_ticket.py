from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from planetarium.models import ShowSession, Ticket, Reservation
from planetarium.serializers import TicketListSerializer
from planetarium.tests.default_test_data import (
    user_test,
    sample_show_theme,
    sample_planetarium_dome,
    sample_astronomy_show,
)

Ticket_URL = reverse("planetarium:tickets-list")


class UnauthenticatedTicketApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(username="default_user", password="tiguti2626")

    def test_auth_required(self):
        res = self.client.get(Ticket_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(
            username="default_user", password="defaultpassword122"
        )
        self.client.force_authenticate(self.user)

    def test_request_user_list(self):
        """Ticket object 1"""
        reservation_object_1 = Reservation.objects.create(user=self.user)

        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        Ticket.objects.create(
            row=40,
            seat=10,
            show_session=show_session_object_1,
            reservation=reservation_object_1,
        )
        """Ticket object 2"""
        reservation_object_2 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=20
        )
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        Ticket.objects.create(
            row=39,
            seat=10,
            show_session=show_session_object_2,
            reservation=reservation_object_2,
        )
        res = self.client.get(Ticket_URL)
        expected_ticket_list = Ticket.objects.filter(
            reservation__user=self.user
        )
        serializer = TicketListSerializer(expected_ticket_list, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_ticket(self):
        """Ticket object 1"""
        reservation_object_1 = Reservation.objects.create(user=self.user)

        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        Ticket.objects.create(
            row=40,
            seat=10,
            show_session=show_session_object_1,
            reservation=reservation_object_1,
        )
        """Ticket object 2"""
        reservation_object_2 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 2",
            description="New description 2",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=20
        )
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        Ticket.objects.create(
            row=39,
            seat=10,
            show_session=show_session_object_2,
            reservation=reservation_object_2,
        )

        res = self.client.get(Ticket_URL)
        ticket_list = Ticket.objects.all()
        serializer = TicketListSerializer(ticket_list, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_not_create_ticket(self):
        """Ticket object 1"""

        reservation_object_1 = Reservation.objects.create(user=self.user)

        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )

        payload = {
            "row": 40,
            "seat": 10,
            "show_session": show_session_object_1.id,
            "reservation": reservation_object_1,
        }
        res = self.client.post(Ticket_URL, payload)
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class TicketFilteringApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(
            username="default_user", password="defaultpassword122"
        )
        self.client.force_authenticate(self.user)

    def test_filter_ticket_show_session_astronomy_show_title(self):
        """Ticket object 1"""

        reservation_object_1 = Reservation.objects.create(user=self.user)

        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show test",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticket_object_1 = Ticket.objects.create(
            row=40,
            seat=10,
            show_session=show_session_object_1,
            reservation=reservation_object_1,
        )
        """Ticket object 2"""
        reservation_object_2 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 2 test",
            description="New description 2",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=20
        )
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticket_object_2 = Ticket.objects.create(
            row=39,
            seat=10,
            show_session=show_session_object_2,
            reservation=reservation_object_2,
        )
        """Ticket object 3"""
        reservation_object_3 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 3",
            description="New description 3",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test3"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test3", rows=40, seats_in_row=20
        )
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-21",
        )
        ticket_object_3 = Ticket.objects.create(
            row=38,
            seat=10,
            show_session=show_session_object_3,
            reservation=reservation_object_3,
        )

        res = self.client.get(Ticket_URL, {"show_session": "test"})

        serializer1 = TicketListSerializer(ticket_object_1)
        serializer2 = TicketListSerializer(ticket_object_2)
        serializer3 = TicketListSerializer(ticket_object_3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_ticket_reservation_user(self):
        """Ticket object 1"""

        reservation_object_1 = Reservation.objects.create(user=self.user)

        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show test",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticket_object_1 = Ticket.objects.create(
            row=40,
            seat=10,
            show_session=show_session_object_1,
            reservation=reservation_object_1,
        )
        user2 = user_test(
            username="default_user_1", password="defaultpassword122"
        )
        """Ticket object 2"""
        reservation_object_2 = Reservation.objects.create(user=user2)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 2 test",
            description="New description 2",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=20
        )
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticket_object_2 = Ticket.objects.create(
            row=39,
            seat=10,
            show_session=show_session_object_2,
            reservation=reservation_object_2,
        )

        """Ticket object 3"""
        user3 = user_test(username="NO Match", password="defaultpassword122")

        reservation_object_3 = Reservation.objects.create(user=user3)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 3",
            description="New description 3",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test3"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test3", rows=40, seats_in_row=20
        )
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-21",
        )
        ticket_object_3 = Ticket.objects.create(
            row=38,
            seat=10,
            show_session=show_session_object_3,
            reservation=reservation_object_3,
        )

        res = self.client.get(Ticket_URL, {"reservation": "default"})

        serializer1 = TicketListSerializer(ticket_object_1)
        serializer2 = TicketListSerializer(ticket_object_2)
        serializer3 = TicketListSerializer(ticket_object_3)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_ticket_show_session_planetarium_dome_name(self):
        """Ticket object 1"""

        reservation_object_1 = Reservation.objects.create(user=self.user)

        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show test",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticket_object_1 = Ticket.objects.create(
            row=40,
            seat=10,
            show_session=show_session_object_1,
            reservation=reservation_object_1,
        )
        """Ticket object 2"""
        reservation_object_2 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 2 test",
            description="New description 2",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test1"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test2", rows=40, seats_in_row=20
        )
        show_session_object_2 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticket_object_2 = Ticket.objects.create(
            row=39,
            seat=10,
            show_session=show_session_object_2,
            reservation=reservation_object_2,
        )
        """Ticket object 3"""
        reservation_object_3 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show 3",
            description="New description 3",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test3"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome 3", rows=40, seats_in_row=20
        )
        show_session_object_3 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-21",
        )
        ticket_object_3 = Ticket.objects.create(
            row=38,
            seat=10,
            show_session=show_session_object_3,
            reservation=reservation_object_3,
        )

        res = self.client.get(Ticket_URL, {"planetarium_dome": "test"})
        serializer1 = TicketListSerializer(ticket_object_1)
        serializer2 = TicketListSerializer(ticket_object_2)
        serializer3 = TicketListSerializer(ticket_object_3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)


class TicketValidation(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(
            username="default_user", password="defaultpassword122"
        )
        self.client.force_authenticate(self.user)

    def test_validate_ticket_row_model_range(self):
        """Ticket object 1"""
        with self.assertRaises(ValueError):
            reservation_object_1 = Reservation.objects.create(user=self.user)

            astronomy_show_object = sample_astronomy_show(
                title="New Astronomy Show test",
                description="New description",
            )
            astronomy_show_object.show_theme.add(
                sample_show_theme(name="Test")
            )
            planetarium_dome_object = sample_planetarium_dome(
                name="Planetarium Dome Test1", rows=40, seats_in_row=30
            )
            show_session_object_1 = ShowSession.objects.create(
                astronomy_show=astronomy_show_object,
                planetarium_dome=planetarium_dome_object,
                show_time="2024-05-19",
            )
            Ticket.objects.create(
                row=40,
                seat=10,
                show_session=show_session_object_1,
                reservation=reservation_object_1,
            )

            """Ticket object 2"""
            reservation_object_2 = Reservation.objects.create(user=self.user)
            astronomy_show_object = sample_astronomy_show(
                title="New Astronomy Show 2 test",
                description="New description 2",
            )
            astronomy_show_object.show_theme.add(
                sample_show_theme(name="Test1")
            )
            planetarium_dome_object = sample_planetarium_dome(
                name="Planetarium Dome Test2", rows=40, seats_in_row=20
            )
            show_session_object_2 = ShowSession.objects.create(
                astronomy_show=astronomy_show_object,
                planetarium_dome=planetarium_dome_object,
                show_time="2024-05-19",
            )
            Ticket.objects.create(
                row=51,
                seat=10,
                show_session=show_session_object_2,
                reservation=reservation_object_2,
            )

        """Ticket object 1"""
        with self.assertRaises(ValueError):
            reservation_object_1 = Reservation.objects.create(user=self.user)

            astronomy_show_object = sample_astronomy_show(
                title="New Astronomy Show test",
                description="New description",
            )
            astronomy_show_object.show_theme.add(
                sample_show_theme(name="Test")
            )
            planetarium_dome_object = sample_planetarium_dome(
                name="Planetarium Dome Test1", rows=40, seats_in_row=30
            )
            show_session_object_1 = ShowSession.objects.create(
                astronomy_show=astronomy_show_object,
                planetarium_dome=planetarium_dome_object,
                show_time="2024-05-19",
            )
            Ticket.objects.create(
                row=40,
                seat=10,
                show_session=show_session_object_1,
                reservation=reservation_object_1,
            )

            """Ticket object 2"""
            reservation_object_2 = Reservation.objects.create(user=self.user)
            astronomy_show_object = sample_astronomy_show(
                title="New Astronomy Show 2 test",
                description="New description 2",
            )
            astronomy_show_object.show_theme.add(
                sample_show_theme(name="Test1")
            )
            planetarium_dome_object = sample_planetarium_dome(
                name="Planetarium Dome Test2", rows=40, seats_in_row=20
            )
            show_session_object_2 = ShowSession.objects.create(
                astronomy_show=astronomy_show_object,
                planetarium_dome=planetarium_dome_object,
                show_time="2024-05-19",
            )
            Ticket.objects.create(
                row=50,
                seat=10,
                show_session=show_session_object_2,
                reservation=reservation_object_2,
            )

    def test_validate_ticket_seat_range_model(self):
        with self.assertRaises(ValueError):
            """Ticket object 1"""
            reservation_object_1 = Reservation.objects.create(user=self.user)
            astronomy_show_object = sample_astronomy_show(
                title="New Astronomy Show test",
                description="New description",
            )
            astronomy_show_object.show_theme.add(
                sample_show_theme(name="Test")
            )
            planetarium_dome_object = sample_planetarium_dome(
                name="Planetarium Dome Test1", rows=40, seats_in_row=30
            )
            show_session_object_1 = ShowSession.objects.create(
                astronomy_show=astronomy_show_object,
                planetarium_dome=planetarium_dome_object,
                show_time="2024-05-19",
            )
            Ticket.objects.create(
                row=40,
                seat=31,
                show_session=show_session_object_1,
                reservation=reservation_object_1,
            )

            """Ticket object 2"""
            reservation_object_2 = Reservation.objects.create(user=self.user)
            astronomy_show_object = sample_astronomy_show(
                title="New Astronomy Show 2 test",
                description="New description 2",
            )
            astronomy_show_object.show_theme.add(
                sample_show_theme(name="Test1")
            )
            planetarium_dome_object = sample_planetarium_dome(
                name="Planetarium Dome Test2", rows=40, seats_in_row=20
            )
            show_session_object_2 = ShowSession.objects.create(
                astronomy_show=astronomy_show_object,
                planetarium_dome=planetarium_dome_object,
                show_time="2024-05-19",
            )
            Ticket.objects.create(
                row=39,
                seat=10,
                show_session=show_session_object_2,
                reservation=reservation_object_2,
            )


class TicketModelsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(
            username="default_user", password="defaultpassword122"
        )
        self.client.force_authenticate(self.user)

    def test_show_theme_str(self):
        """Ticket object 1"""
        reservation_object_1 = Reservation.objects.create(user=self.user)
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show test",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        ticker_object = Ticket.objects.create(
            row=40,
            seat=30,
            show_session=show_session_object_1,
            reservation=reservation_object_1,
        )

        self.assertEqual(
            ticker_object.__str__(),
            f"row:{ticker_object.row} - seat:{ticker_object.seat} - show_session:{ticker_object.show_session} - reservation:{ticker_object.reservation.user}",
        )


class ReservationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = user_test(
            username="default_user", password="defaultpassword122"
        )
        self.user_1 = user_test(username="bad_user", password="bad122")
        self.client.force_authenticate(self.user)

    def test_ticket_not_create_with_reservation(self):
        self.client.force_authenticate(None)
        reservation_invalid_object = Reservation.objects.create(
            user=self.user_1
        )
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show test",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        data = {
            "row": 40,
            "seat": 30,
            "show_session": show_session_object_1.id,
            "reservation": reservation_invalid_object.id,
        }
        response = self.client.post(Ticket_URL, data)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ticket_create_with_reservation(self):
        reservation_invalid_object = Reservation.objects.create(
            user=self.user
        )
        astronomy_show_object = sample_astronomy_show(
            title="New Astronomy Show test",
            description="New description",
        )
        astronomy_show_object.show_theme.add(sample_show_theme(name="Test"))
        planetarium_dome_object = sample_planetarium_dome(
            name="Planetarium Dome Test1", rows=40, seats_in_row=30
        )
        show_session_object_1 = ShowSession.objects.create(
            astronomy_show=astronomy_show_object,
            planetarium_dome=planetarium_dome_object,
            show_time="2024-05-19",
        )
        data = {
            "row": 40,
            "seat": 30,
            "show_session": show_session_object_1.id,
            "reservation": reservation_invalid_object.id,
        }
        response = self.client.post(Ticket_URL, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
