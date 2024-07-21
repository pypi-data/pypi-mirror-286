from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class DynamicColumnsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "dynamic_columns"
    verbose_name = _("Admin dynamic columns")
