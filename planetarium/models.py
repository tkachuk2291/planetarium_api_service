from django.db import models
from planetarium_api_service import settings


class AstronomyShow(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    show_theme = models.ManyToManyField("ShowTheme", related_name="astronomy_shows")


class ShowTheme(models.Model):
    name = models.CharField(max_length=256)


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name="show_sessions")
    planetarium = models.ForeignKey("PlanetariumDome", on_delete=models.CASCADE, related_name="dome_sessions")
    show_time = models.DateTimeField()


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=256)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="reservation_tickets")


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
