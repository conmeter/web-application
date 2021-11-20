import re

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
import urllib.request
from django.core.exceptions import ValidationError
from pip._vendor import requests


def validate_url(url):
    try:
        urll = url.lower()
        m1 = "http://"
        m2 = "https://"
        m3 = "www."
        if m1 not in urll and m2 not in urll and m3 in urll:
            urll = m1 + urll
        elif m1 not in urll and m2 not in urll and m3 not in urll:
            urll = m1 + m3 + urll
        r = requests.head(urll)
    except Exception:
        raise ValidationError("URL does not exist")


class Webs(models.Model):
    url = models.CharField(primary_key=True, max_length=255, validators=[validate_url])
    name = models.CharField(unique=True, blank=False, max_length=255)
    desc = models.CharField(null=False, blank=False, max_length=500)

    def __str__(self):
        return self.name
