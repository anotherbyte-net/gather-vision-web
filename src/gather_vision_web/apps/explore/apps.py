from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ExploreAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gather_vision_web.apps.explore"
    verbose_name = _("Explore")
