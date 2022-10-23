from django.db import models

from gather_vision_web.apps.explore.models import Origin, Coordinate, Area


class StationManager(models.Manager):
    def get_by_natural_key(self, name, origin):
        return self.get(name=name, origin=origin)


class Station(models.Model):
    """A water measurement station."""

    origin = models.ForeignKey(
        Origin,
        related_name="water_stations",
        on_delete=models.CASCADE,
    )
    area = models.ForeignKey(
        Area,
        blank=True,
        null=True,
        related_name="water_stations",
        on_delete=models.PROTECT,
    )
    coordinate = models.ForeignKey(
        Coordinate,
        blank=True,
        null=True,
        related_name="water_stations",
        on_delete=models.PROTECT,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="The date this record was created.",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text="The date this record was most recently modified.",
    )
    name = models.SlugField(
        help_text="The name of the event.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The displayed title.",
    )
    description = models.TextField(
        help_text="The description of the origin.",
    )

    objects = StationManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["origin", "name"],
                name="water_station_unique_origin_name",
            )
        ]

    def natural_key(self):
        return (self.name,) + self.origin.natural_key()

    natural_key.dependencies = ["explore.origin"]

    def __str__(self):
        return f"water station {self.title} ({self.name})"


class GroupManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Group(models.Model):
    """A named collection of measurements."""

    created_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="The date this record was created.",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text="The date this record was most recently modified.",
    )
    name = models.SlugField(
        help_text="The name of the event.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The displayed title.",
    )

    objects = GroupManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="water_group_unique_name",
            )
        ]

    def natural_key(self):
        return (self.name,)

    natural_key.dependencies = []

    def __str__(self):
        return f"group {self.title} ({self.name})"


class MeasureManager(models.Manager):
    def get_by_natural_key(self, issued_date, station):
        return self.get(issued_date=issued_date, station=station)


class Measure(models.Model):
    """A measure at a station."""

    OBSERVED_HEIGHT = "observed_height"
    OBTAINED_SAMPLE = "obtained_sample"
    FORECAST_HEIGHT = "forecast_height"
    THRESHOLD = "threshold"
    CATEGORY_CHOICES = [
        (OBSERVED_HEIGHT, "Observed height"),
        (OBTAINED_SAMPLE, "Obtained sample"),
        (FORECAST_HEIGHT, "Forecast height"),
        (THRESHOLD, "Threshold"),
    ]

    VALID = "valid"
    INVALID = "invalid"
    NOT_TESTED = "not_tested"
    WARN_MINOR = "warn_minor"
    WARN_MODERATE = "warn_moderate"
    WARN_MAJOR = "warn_major"
    QUALITY_CHOICES = [
        (VALID, "Valid"),
        (INVALID, "Invalid"),
        (NOT_TESTED, "Not tested"),
        (WARN_MINOR, "Minor warning"),
        (WARN_MODERATE, "Moderate warning"),
        (WARN_MAJOR, "Major warning"),
    ]

    station = models.ForeignKey(
        Station,
        related_name="measurements",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        related_name="measurements",
        on_delete=models.PROTECT,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        help_text="The date this record was created.",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        editable=False,
        help_text="The date this record was most recently modified.",
    )
    issued_date = models.DateTimeField(
        editable=False,
        help_text="The date this record was issued.",
    )
    retrieved_date = models.DateTimeField(
        editable=False,
        help_text="The date this record was retrieved.",
    )
    occurred_date = models.DateTimeField(
        editable=False,
        help_text="The date this record occurred.",
    )
    level = models.FloatField(
        blank=True,
        null=True,
        help_text="The value of the measurement.",
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="The measure type.",
    )
    quality = models.CharField(
        max_length=20,
        choices=QUALITY_CHOICES,
        help_text="The measure quality or status.",
    )

    objects = MeasureManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["occurred_date", "station"],
                name="water_measure_unique_occurred_date_station",
            )
        ]

    def natural_key(self):
        return (self.occurred_date,) + self.station.natural_key()

    natural_key.dependencies = ["water.station"]

    def __str__(self):
        return (
            f"measure {self.level} at {self.occurred_date} "
            f"({self.get_category_display()} - {self.get_quality_display()})"
        )
