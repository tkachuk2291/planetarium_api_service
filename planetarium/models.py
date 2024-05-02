from django.db import models
from django.db.models import UniqueConstraint

from planetarium_api_service import settings


class AstronomyShow(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    show_theme = models.ManyToManyField("ShowTheme", related_name="astronomy_shows")


class ShowTheme(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name'], name='unique_name')
        ]


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(AstronomyShow, on_delete=models.CASCADE, related_name="show_sessions")
    planetarium_dome = models.ForeignKey("PlanetariumDome", on_delete=models.CASCADE, related_name="dome_sessions")
    show_time = models.DateField()


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=256)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name'], name='unique_name_planetarium')
        ]

    @staticmethod
    def validate_row_seats_in_row(rows, seats_in_row, error_to_raise):
        if not 1 <= rows <= 50:
            raise error_to_raise(
                "Set the actual number of rows in the planetarium! The maximum available value is 50 rows.")
        if not 1 <= seats_in_row <= 630:
            raise error_to_raise(
                "Set the actual number of seats in the planetarium! The maximum available value is 630 rows.")

    def clean(self):
        PlanetariumDome.validate_row_seats_in_row(self.rows, self.seats_in_row, ValueError)

    def save(self, force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.full_clean()
        return super(PlanetariumDome, self).save(force_insert, force_update, using, update_fields)


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(ShowSession, on_delete=models.CASCADE, related_name="tickets")
    reservation = models.ForeignKey("Reservation", on_delete=models.CASCADE, related_name="reservation_tickets")

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat"], name="unique_row_seats")
        ]

    @staticmethod
    def validate_seats_row(row, num_row, seat, num_seats_in_row, error_to_raise):
        if not 1 <= row <= num_row:
            raise error_to_raise("the row must be from 1 to {}".format(num_row))
        if not 1 <= seat <= num_seats_in_row:
            raise error_to_raise(
                "the seat must be from 1 to  {}".format(num_seats_in_row))

    def clean(self):
        Ticket.validate_seats_row(self.row,
                                  self.show_session.planetarium_dome.rows,
                                  self.seat,
                                  self.show_session.planetarium_dome.seats_in_row, ValueError
                                  )

    def save(self, force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.full_clean()
        return super(Ticket, self).save(force_insert, force_update, using, update_fields)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
