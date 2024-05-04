from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from planetarium.models import (
    Ticket, Reservation, ShowSession, AstronomyShow, PlanetariumDome, ShowTheme,
)
from user.models import User
from user.serializers import UserSerializer

"""Basic serializers"""


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ("title", "description", "show_theme")


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ("name",)


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time")


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = PlanetariumDome
        fields = ("rows", "seats_in_row", "image")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("created_at", "user")


"""Custom Serializers for model Ticket"""


class TicketListSerializer(TicketSerializer):
    show_session = serializers.CharField(source="show_session.astronomy_show.title", read_only=True)
    reservation = serializers.CharField(source="reservation.user", read_only=True)
    planetarium_dome = serializers.CharField(source="show_session.planetarium_dome.name", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation", "planetarium_dome")


class TicketCreateSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session")
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(),
                fields=['row', 'seat']
            )
        ]

    def validate(self, attrs):
        Ticket.validate_seats_row(
            attrs["row"],
            attrs["show_session"].planetarium_dome.rows,
            attrs["seat"],
            attrs["show_session"].planetarium_dome.seats_in_row,
            serializers.ValidationError
        )
        return attrs


class UserTicketSerializer(UserSerializer):
    reservation_for = serializers.CharField(source="username")

    class Meta:
        model = User
        fields = ("reservation_for",)


class ReservationDetailSerializer(ReservationSerializer):
    visitor = UserTicketSerializer(source="user")

    class Meta:
        model = Reservation
        fields = ("created_at", "visitor")


class PlanetariumDomeTicketSerializer(PlanetariumDomeSerializer):
    planetarium_name = serializers.CharField(source="name")

    class Meta:
        model = PlanetariumDome
        fields = ("planetarium_name",)


class AstronomyShowTicketSerializer(AstronomyShowSerializer):
    show_name = serializers.CharField(source="title")
    show_theme = serializers.SerializerMethodField()

    class Meta:
        model = AstronomyShow
        fields = ("show_name", "show_theme")

    @staticmethod
    def get_show_theme(obj):
        show_themes = obj.show_theme.all()
        return [theme.name for theme in show_themes]


class ShowSessionTicketSerializer(serializers.ModelSerializer):
    planetarium_dome = PlanetariumDomeTicketSerializer()
    astronomy_show = AstronomyShowTicketSerializer()

    class Meta:
        model = ShowSession
        fields = ("show_time", "planetarium_dome", "astronomy_show")


class TicketDetailSerializer(serializers.ModelSerializer):
    reservation = ReservationDetailSerializer()
    show_session = ShowSessionTicketSerializer()

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "show_session", "reservation")


"""Custom Serializers for model Astronomy"""


class AstronomyShowListSerializer(AstronomyShowSerializer):
    show_name = serializers.CharField(source="title", read_only=True)
    show_theme = ShowThemeSerializer(many=True, read_only=True)

    class Meta:
        model = AstronomyShow
        fields = ("show_name", "description", "show_theme", "image")


class AstronomyShowCreateSerializer(AstronomyShowSerializer):
    title = serializers.CharField(validators=[UniqueValidator(
        queryset=AstronomyShow.objects.all())])

    class Meta:
        model = AstronomyShow
        fields = ("title", "description", "show_theme", "image")


class AstronomyShowImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "image")


"""Custom Serializers for model Planetarium Dome"""


class PlanetariumDomeListSerializer(PlanetariumDomeSerializer):
    planetarium_name = serializers.CharField(source="name", read_only=True)

    class Meta:
        model = PlanetariumDome
        fields = ("planetarium_name", "rows", "seats_in_row", "image")


class PlanetariumDomeCreateSerializer(PlanetariumDomeSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(
            queryset=PlanetariumDome.objects.all())]
    )

    class Meta:
        model = PlanetariumDome
        fields = ("name", "rows", "seats_in_row", "image")

    def validate(self, attrs):
        PlanetariumDome.validate_row_seats_in_row(
            attrs["rows"],
            attrs["seats_in_row"],
            serializers.ValidationError
        )
        return attrs


class PlanetariumDomeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ("id", "image")


"""Custom Serializers for model ShowSessionSerializer"""


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowListSerializer(read_only=True)
    planetarium_dome = PlanetariumDomeListSerializer(read_only=True)

    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time")


class ShowSessionCreateSerializer(ShowSessionSerializer):
    class Meta:
        model = ShowSession
        fields = ("astronomy_show", "planetarium_dome", "show_time")


class ShowThemeCreateSerializer(ShowThemeSerializer):
    name = serializers.CharField(validators=[UniqueValidator(
        queryset=ShowTheme.objects.all())]
    )

    class Meta:
        model = ShowTheme
        fields = ("name",)
