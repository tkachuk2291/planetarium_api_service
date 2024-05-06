from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from planetarium.models import (
    Ticket,
    AstronomyShow,
    PlanetariumDome,
    ShowSession,
    Reservation,
    ShowTheme,
)
from planetarium.permissions import IsAdminOrIfAuthenticatedReadOnly
from planetarium.serializers import (
    TicketSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
    TicketListSerializer,
    AstronomyShowListSerializer,
    AstronomyShowCreateSerializer,
    PlanetariumDomeListSerializer,
    PlanetariumDomeCreateSerializer,
    ShowSessionListSerializer,
    ShowSessionCreateSerializer,
    ShowThemeSerializer,
    PlanetariumDomeImageSerializer,
    AstronomyShowImageSerializer,
)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketDetailSerializer
        elif self.action == "create":
            return TicketCreateSerializer
        return TicketListSerializer

    """filtering for query_params 'show_session', 'reservation' , 'planetarium_dome' """

    def get_queryset(self):
        show_session = self.request.query_params.get("show_session")
        reservation = self.request.query_params.get("reservation")
        planetarium_dome = self.request.query_params.get("planetarium_dome")

        queryset = self.queryset
        if show_session:
            queryset = queryset.filter(
                show_session__astronomy_show__title__icontains=show_session
            )
        if reservation:
            queryset = queryset.filter(
                reservation__user__username__icontains=reservation
            )
        if planetarium_dome:
            queryset = queryset.filter(
                show_session__planetarium_dome__name__icontains=planetarium_dome
            )
        return queryset.filter(reservation__user=self.request.user).distinct()

    def perform_create(self, serializer):
        reservation_obj = Reservation.objects.create(user=self.request.user)
        serializer.save(reservation=reservation_obj)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="show_session",
                type=OpenApiTypes.STR,
                description="Filter by show_session show_session(title)",
            ),
            OpenApiParameter(
                name="reservation",
                type=OpenApiTypes.STR,
                description="Filter by reservation(username)",
            ),
            OpenApiParameter(
                name="planetarium_dome",
                type=OpenApiTypes.STR,
                description="Filter by planetarium_dome(name)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """filtering for query_params 'show_session', 'reservation' , 'planetarium_dome'"""
        return super().list(request, *args, **kwargs)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all().prefetch_related("show_theme")
    serializer_class = AstronomyShowListSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return AstronomyShowListSerializer
        elif self.action == "upload_image":
            return AstronomyShowImageSerializer
        return AstronomyShowCreateSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request):
        astronomy_show = self.get_object()
        serializer = self.get_serializer(astronomy_show, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """filtering for query_params 'title', 'description' , 'show_theme' """

    def get_queryset(self):
        astronomy_show_show_theme = self.request.query_params.get(
            "show_theme"
        )
        astronomy_show_show_name = self.request.query_params.get("show_name")
        astronomy_show_description = self.request.query_params.get(
            "description"
        )

        queryset = self.queryset
        if astronomy_show_show_theme:
            queryset = queryset.filter(
                show_theme__name__icontains=astronomy_show_show_theme
            )
        if astronomy_show_show_name:
            queryset = queryset.filter(
                title__icontains=astronomy_show_show_name
            )
        if astronomy_show_description:
            queryset = queryset.filter(
                description__icontains=astronomy_show_description
            )
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="show_theme",
                type=OpenApiTypes.STR,
                description="Filter by show_theme(name)",
            ),
            OpenApiParameter(
                name="reservation",
                type=OpenApiTypes.STR,
                description="Filter by show_name(title)",
            ),
            OpenApiParameter(
                name="description",
                type=OpenApiTypes.STR,
                description="Filter by description(description)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """filtering for query_params 'title', 'description' , 'show_theme'"""
        return super().list(request, *args, **kwargs)


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeListSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    """filtering for query_params 'planetarium_name' , 'rows' , 'seats_in_row' """

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

    def get_serializer_class(self):
        if self.action == "list":
            return PlanetariumDomeListSerializer
        elif self.action == "upload_image":
            return PlanetariumDomeImageSerializer
        return PlanetariumDomeCreateSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request):
        bus = self.get_object()
        serializer = self.get_serializer(bus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="planetarium_name",
                type=OpenApiTypes.STR,
                description="Filter by planetarium_name(name)",
            ),
            OpenApiParameter(
                name="rows",
                type=OpenApiTypes.INT,
                description="Filter by rows(rows)",
            ),
            OpenApiParameter(
                name="seats_in_row",
                type=OpenApiTypes.INT,
                description="Filter by seats_in_row(seats_in_row)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """filtering for query_params 'planetarium_name' , 'rows' , 'seats_in_row'"""
        return super().list(request, *args, **kwargs)


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all().select_related(
        "astronomy_show", "planetarium_dome"
    )
    serializer_class = ShowSessionListSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return ShowSessionListSerializer
        return ShowSessionCreateSerializer

    """filtering for query_params 'show_name', 'description' , 'name' """

    def get_queryset(self):
        astronomy_show_title = self.request.query_params.get("show_name")
        astronomy_show_description = self.request.query_params.get(
            "description"
        )
        planetarium_dome = self.request.query_params.get("name")
        show_time = self.request.query_params.get("show_time")

        queryset = self.queryset
        if astronomy_show_title:
            queryset = queryset.filter(
                astronomy_show__title__icontains=astronomy_show_title
            )
        if astronomy_show_description:
            queryset = queryset.filter(
                astronomy_show__description__icontains=astronomy_show_description
            )
        if planetarium_dome:
            queryset = queryset.filter(
                planetarium_dome__name__icontains=planetarium_dome
            )
        if show_time:
            queryset = queryset.filter(show_time__exact=show_time)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="show_name",
                type=OpenApiTypes.STR,
                description="Filter by show_name(name)",
            ),
            OpenApiParameter(
                name="description",
                type=OpenApiTypes.STR,
                description="Filter by description(description)",
            ),
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                description="Filter by name(name)",
            ),
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.DATE,
                description="Filter by show_time(show_time)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """filtering for query_params 'show_name', 'description' , 'name'"""
        return super().list(request, *args, **kwargs)


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer
    permission_classes = [IsAdminOrIfAuthenticatedReadOnly]
    """filtering for query_params 'name' """

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type=OpenApiTypes.STR,
                description="Filter by name(name)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """filtering for query_params 'name'"""
        return super().list(request, *args, **kwargs)
