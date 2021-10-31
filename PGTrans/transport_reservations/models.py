from enum import Enum

from django.core.validators import RegexValidator
from django.db import models
from djmoney.models.fields import MoneyField

from django.contrib.auth.models import AbstractUser

from django.conf import settings

CHAR_FIELD_LENGTH = 100


class Choices(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Authority(Choices):
    PASSENGER = "PASSENGER"
    DRIVER = "DRIVER"


phone_regex = RegexValidator(
    regex=r'^\+\d{8,15}$',
    message=("Phone number must be entered in the format: "
             "'+999999999'. Up to 15 digits allowed.")
)


class User(AbstractUser):
    authority = models.CharField(max_length=CHAR_FIELD_LENGTH, choices=Authority.choices())
    phone = models.CharField(validators=[phone_regex], max_length=16, blank=True)


def get_user_foreign_key():
    return models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class TransportStatus(Choices):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELED = "CANCELED"
    FINISHED = "FINISHED"


class Vehicle(models.Model):
    driver = get_user_foreign_key()
    registration_number = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=20)

    def __str__(self) -> str:
        return f"{self.color} {self.model} of {self.driver.name}"


class Transport(models.Model):
    driver = get_user_foreign_key()
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
    )
    departure_time = models.DateTimeField()
    departure_address = models.CharField(max_length=CHAR_FIELD_LENGTH)
    destination = models.CharField(max_length=CHAR_FIELD_LENGTH)
    meeting_place = models.CharField(max_length=CHAR_FIELD_LENGTH)
    state = models.CharField(max_length=255, choices=TransportStatus.choices())
    cost = MoneyField(max_digits=10, decimal_places=2, default_currency='CZK')
    max_passengers = models.IntegerField()

    def __str__(self) -> str:
        return f"Transport of {self.driver.name} to {self.departure_address} at {self.departure_time}"


class Request(models.Model):
    passenger = get_user_foreign_key()
    from_time = models.DateTimeField()
    to_time = models.DateTimeField()
    destination = models.CharField(max_length=CHAR_FIELD_LENGTH)
    number_of_passengers = models.IntegerField()

    def __str__(self) -> str:
        return f"Request from {self.passenger.name} for {self.destination} at {self.from_time}"


class Reservation(models.Model):
    transport = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,
    )
    passenger = get_user_foreign_key()

    def __str__(self) -> str:
        return f"{self.transport} for {self.passenger.name}"
