from rest_framework import viewsets

from planetarium.models import Ticket, AstronomyShow, PlanetariumDome, ShowSession
from planetarium.serializers import TicketSerializer, TicketDetailSerializer, TicketCreateSerializer, \
    TicketListSerializer, AstronomyShowListSerializer, AstronomyShowCreateSerializer, PlanetariumDomeListSerializer, \
    PlanetariumDomeCreateSerializer, ShowSessionListSerializer, ShowSessionCreateSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'retrieve':
            return TicketDetailSerializer
        elif self.action == 'create':
            return TicketCreateSerializer
        return TicketListSerializer


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return AstronomyShowListSerializer
        return AstronomyShowCreateSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return PlanetariumDomeListSerializer
        return PlanetariumDomeCreateSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionListSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return ShowSessionListSerializer
        return ShowSessionCreateSerializer
