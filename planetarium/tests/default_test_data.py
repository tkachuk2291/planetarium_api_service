from xxlimited_35 import Null

from django.contrib.auth import get_user_model

from planetarium.models import ShowTheme, AstronomyShow, PlanetariumDome, Ticket, ShowSession


def sample_show_theme(**params):
    defaults = {
        "name": "Sample Theme"
    }
    defaults.update(params)
    return ShowTheme.objects.create(**params)


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample Astronomy Show",
        "description": "Sample description",
    }
    defaults.update(params)
    astronomy_show_obj = AstronomyShow.objects.create(**defaults)
    return astronomy_show_obj


def sample_planetarium_dome(**params):
    defaults = {
        "name": "Sample Planetarium Dome",
        "rows": 30,
        "seats_in_row": 250,
    }
    defaults.update(params)
    return PlanetariumDome.objects.create(**defaults)


def sample_show_session(**params):
    defaults = {
        "astronomy_show": sample_astronomy_show(),
        "planetarium_dome": sample_planetarium_dome(),
        "show_time": "2024-05-19"
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


def sample_ticket(**params):
    defaults = {
        "row": 1,
        "seats_in_row": 2,
        "show_session": sample_show_session()
    }
    defaults.update(params)
    return Ticket.objects.create(**defaults)


def user_test(**params):
    defaults = {
        'username': 'default_user',
        'email': 'default@example.com',
        'password': 'default_password'
    }
    defaults.update(params)
    user = get_user_model().objects.create_user(**defaults)
    return user

