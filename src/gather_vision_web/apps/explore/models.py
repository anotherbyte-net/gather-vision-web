from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class CoordinateManager(models.Manager):
    def get_by_natural_key(self, latitude, longitude, reference_system):
        return self.get(
            latitude=latitude, longitude=longitude, reference_system=reference_system
        )


class Coordinate(models.Model):
    """A geographic coordinate."""

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
    latitude = models.DecimalField(
        max_digits=7,
        decimal_places=5,
        help_text="The latitude (North/South position, -90 to +90).",
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        help_text="The longitude (East/West position -180 to +180).",
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    reference_system = models.SlugField(
        blank=True,
        help_text="The geographic spatial reference system for the coordinates.",
    )

    objects = CoordinateManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["latitude", "longitude", "reference_system"],
                name="explore_coordinate_unique_latitude_longitude_ref",
            )
        ]

    def natural_key(self):
        return self.latitude, self.longitude, self.reference_system

    natural_key.dependencies = []

    def __str__(self):
        return f"{self.latitude},{self.longitude} ({self.reference_system})"


class AreaManager(models.Manager):
    def get_by_natural_key(self, name, level, parent):
        return self.get(name=name, level=level, parent=parent)


class Area(models.Model):
    """A known geographical location."""

    # region = administrative division / state / province
    # district = county / sub-administrative division
    # locality = city / town
    # neighbourhood = suburb / dependent locality

    COUNTRY = "L1"
    REGION = "L2"
    DISTRICT = "L3"
    LOCALITY = "L4"
    NEIGHBOURHOOD = "L5"
    LEVEL_CHOICES = [
        (COUNTRY, "Country (level 1)"),
        (REGION, "Region (level 2)"),
        (DISTRICT, "District (level 3)"),
        (LOCALITY, "Locality (level 4)"),
        (NEIGHBOURHOOD, "Neighbourhood (level 5)"),
    ]

    parent = models.ForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text="The parent area that contains this area.",
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
        help_text="The name of the area.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The displayed title.",
    )
    level = models.CharField(
        max_length=2,
        choices=LEVEL_CHOICES,
        help_text="The division level.",
    )

    objects = AreaManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "level", "parent"],
                name="explore_area_unique_name_level_parent",
            )
        ]

    def natural_key(self):
        return self.name, self.level, self.parent

    natural_key.dependencies = ["explore.area"]

    def __str__(self):
        return f"{self.title} ({self.name},{self.get_level_display()})"


class OriginManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Origin(models.Model):
    """"""

    area = models.ForeignKey(
        Area,
        blank=True,
        null=True,
        related_name="origins",
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
        help_text="The name of the origin.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The displayed title.",
    )
    description = models.TextField(
        help_text="The description of the origin.",
    )
    url = models.URLField(
        blank=True,
        help_text="A link to origin details.",
    )

    objects = OriginManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="explore_area_unique_name",
            )
        ]

    def natural_key(self):
        return (self.name,)

    natural_key.dependencies = []

    def __str__(self):
        return f"{self.title} ({self.name})"
