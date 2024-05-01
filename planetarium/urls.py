from django.urls import path, include
from rest_framework.routers import DefaultRouter
from planetarium.views import TicketViewSet, AstronomyShowViewSet, PlanetariumDomeViewSet, ShowSessionViewSet, \
    ShowThemeViewSet

router = DefaultRouter()

router.register('tickets', TicketViewSet, basename='tickets')
router.register('astronomy_show', AstronomyShowViewSet, basename='astronomy_show')
router.register('planetarium_dome', PlanetariumDomeViewSet, basename='planetarium_dome')
router.register('show_session', ShowSessionViewSet, basename='show_session')
router.register('show_theme', ShowThemeViewSet, basename='show_theme')


urlpatterns = [
    path("", include(router.urls))
]

app_name = 'planetarium'
