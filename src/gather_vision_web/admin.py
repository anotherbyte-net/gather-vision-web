from django.contrib import admin
from django.utils.translation import gettext as _


class GatherVisionWebAdminSite(admin.AdminSite):
    site_title = _("Gather Vision site admin")
    site_header = _("Gather Vision admin")
    index_title = _("Gather Vision site admin")
