from django.contrib.admin.apps import AdminConfig


class GatherVisionWebAdminConfig(AdminConfig):
    default_site = "gather_vision_web.admin.GatherVisionWebAdminSite"
