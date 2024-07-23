from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MileaUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'milea_users'
    verbose_name = _("User and Groups")
    menu_icon = "ti ti-users-group"
