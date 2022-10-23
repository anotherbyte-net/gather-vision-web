from django.db import models


from gather_vision_web.apps.explore.models import Origin, Coordinate, Area


class GroupManager(models.Manager):
    def get_by_natural_key(self, name, category):
        return self.get(name=name, category=category)


class Group(models.Model):
    """A transport event."""

    BUS = "bus"
    FERRY = "ferry"
    TRAIN = "train"
    TRAM = "tram"
    CATEGORY_CHOICES = [
        (BUS, "Bus"),
        (FERRY, "Ferry"),
        (TRAIN, "Train"),
        (TRAM, "Tram"),
    ]

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
        help_text="The name of the group.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The displayed title.",
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="The type of transport.",
    )
    objects = GroupManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "category"],
                name="transport_group_unique_name_category",
            )
        ]

    def natural_key(self):
        return self.name, self.category

    def __str__(self):
        return f"transport group {self.title} - {self.category} ({self.name})"


class EventManager(models.Manager):
    def get_by_natural_key(self, name, origin):
        return self.get(name=name, origin=origin)


class Event(models.Model):
    """A transport event."""

    TRAIN_TRACK = "train_track"
    TRAIN_STATION = "train_station"
    TRAIN_CARPARK = "train_carpark"
    TRAIN_ACCESSIBILITY = "train_accessibility"
    BUS_STOP = "bus_stop"
    CATEGORY_CHOICES = [
        (TRAIN_TRACK, "Train track"),
        (TRAIN_STATION, "Train station"),
        (TRAIN_CARPARK, "Train carpark"),
        (TRAIN_ACCESSIBILITY, "Train accessibility"),
        (BUS_STOP, "Bus stop"),
    ]

    INFO = "info"
    MINOR = "minor"
    MAJOR = "major"
    SEVERITY_CHOICES = [
        (INFO, "Info"),
        (MINOR, "Minor"),
        (MAJOR, "Major"),
    ]

    origin = models.ForeignKey(
        Origin,
        related_name="transport_events",
        on_delete=models.CASCADE,
    )
    area = models.ForeignKey(
        Area,
        blank=True,
        null=True,
        related_name="transport_events",
        on_delete=models.PROTECT,
    )
    groups = models.ManyToManyField(
        Group,
        related_name="events",
        help_text="The groups involved in this event.",
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
    start_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The date this event started.",
    )
    stop_date = models.DateField(
        blank=True,
        null=True,
        help_text="The date this event stopped.",
    )
    name = models.SlugField(
        help_text="The name of the event.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The displayed title.",
    )
    description = models.TextField(
        help_text="The description of the event.",
    )
    url = models.URLField(
        blank=True,
        help_text="A link to event details.",
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        help_text="The infrastructure affected by the event.",
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        help_text="The severity of the event.",
    )
    locations = models.CharField(
        blank=True,
        max_length=500,
        help_text="The locations covered by the event.",
    )

    objects = EventManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["origin", "name"],
                name="transport_event_unique_origin_name",
            )
        ]

    def natural_key(self):
        return (self.name,) + self.origin.natural_key()

    natural_key.dependencies = ["explore.origin"]

    def __str__(self):
        return f"transport event {self.title} ({self.name})"
