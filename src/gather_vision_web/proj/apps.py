from django.contrib.admin.apps import SimpleAdminConfig


class GatherVisionAdminConfig(SimpleAdminConfig):
    default_site = "gather_vision_web.proj.admin.GatherVisionAdminSite"
