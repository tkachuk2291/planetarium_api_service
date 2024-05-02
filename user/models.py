import pathlib
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


def image_path(self, filename):
    filename = f'{slugify(self.username)}-{uuid.uuid4()}' + pathlib.Path(filename).suffix
    return pathlib.Path("upload/user/avatar") / pathlib.Path(filename)


class User(AbstractUser):
    image = models.ImageField(upload_to=image_path, null=True)

