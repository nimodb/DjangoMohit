from django.db import models


# Create your models here.
class Country(models.Model):
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name"]

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class State(models.Model):
    class Meta:
        ordering = ["country", "name"]

    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="states"
    )

    def __str__(self):
        return self.name


class District(models.Model):
    class Meta:
        ordering = ["state", "name"]

    name = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["district", "name"]

    name = models.CharField(max_length=100, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
