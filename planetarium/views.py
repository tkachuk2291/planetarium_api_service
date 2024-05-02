from rest_framework import viewsets

from planetarium.models import Ticket, AstronomyShow, PlanetariumDome, ShowSession, Reservation, ShowTheme
from planetarium.serializers import TicketSerializer, TicketDetailSerializer, TicketCreateSerializer, \
    TicketListSerializer, AstronomyShowListSerializer, AstronomyShowCreateSerializer, PlanetariumDomeListSerializer, \
    PlanetariumDomeCreateSerializer, ShowSessionListSerializer, ShowSessionCreateSerializer, ShowThemeSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'retrieve':
            return TicketDetailSerializer
        elif self.action == 'create':
            return TicketCreateSerializer
        return TicketListSerializer

    """filtering for query_params 'show_session', 'reservation' , 'planetarium_dome' """

    def get_queryset(self):
        show_session = self.request.query_params.get("show_session")
        reservation = self.request.query_params.get("reservation")
        planetarium_dome = self.request.query_params.get("planetarium_dome")

        queryset = self.queryset
        if show_session:
            queryset = queryset.filter(show_session__astronomy_show__title__icontains=show_session)
        if reservation:
            queryset = queryset.filter(reservation__user__username__icontains=reservation)
        if planetarium_dome:
            queryset = queryset.filter(show_session__planetarium_dome__name__icontains=planetarium_dome)
        return queryset.filter(reservation__user=self.request.user).distinct()

    def perform_create(self, serializer):
        reservation_obj = Reservation.objects.create(user=self.request.user)
        serializer.save(reservation=reservation_obj)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all().prefetch_related('show_theme')
    serializer_class = AstronomyShowListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AstronomyShowListSerializer
        return AstronomyShowCreateSerializer

    """filtering for query_params 'title', 'description' , 'show_theme' """

    def get_queryset(self):
        astronomy_show_show_theme = self.request.query_params.get("show_theme")
        astronomy_show_show_name = self.request.query_params.get("show_name")
        astronomy_show_description = self.request.query_params.get("description")

        queryset = self.queryset
        if astronomy_show_show_theme:
            queryset = queryset.filter(show_theme__name__icontains=astronomy_show_show_theme)
        if astronomy_show_show_name:
            queryset = queryset.filter(title__icontains=astronomy_show_show_name)
        if astronomy_show_description:
            queryset = queryset.filter(description__icontains=astronomy_show_description)
        return queryset.distinct()


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeListSerializer
    """filtering for query_params 'planetarium_name' , 'rows' , 'seats_in_row' """

    def get_serializer_class(self):
        if self.action == 'list':
            return PlanetariumDomeListSerializer
        return PlanetariumDomeCreateSerializer

    def get_queryset(self):
        planetarium_name = self.request.query_params.get("planetarium_name")
        rows = self.request.query_params.get("rows")
        seats_in_row = self.request.query_params.get("seats_in_row")

        queryset = self.queryset
        if planetarium_name:
            queryset = queryset.filter(name__icontains=planetarium_name)
        if rows:
            queryset = queryset.filter(rows=rows)
        if seats_in_row:
            queryset = queryset.filter(seats_in_row=seats_in_row)
        return queryset.distinct()


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related("astronomy_show", "planetarium_dome")
    serializer_class = ShowSessionListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowSessionListSerializer
        return ShowSessionCreateSerializer

    """filtering for query_params 'show_name', 'description' , 'name' """

    def get_queryset(self):
        astronomy_show_title = self.request.query_params.get("show_name")
        astronomy_show_description = self.request.query_params.get("description")
        planetarium_dome = self.request.query_params.get("name")
        show_time = self.request.query_params.get("show_time")

        queryset = self.queryset
        if astronomy_show_title:
            queryset = queryset.filter(astronomy_show__title__icontains=astronomy_show_title)
        if astronomy_show_description:
            queryset = queryset.filter(astronomy_show__description__icontains=astronomy_show_description)
        if planetarium_dome:
            queryset = queryset.filter(planetarium_dome__name__icontains=planetarium_dome)
        if show_time:
            queryset = queryset.filter(show_time__exact=show_time)
        return queryset.distinct()


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    """filtering for query_params 'name' """

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.distinct()
