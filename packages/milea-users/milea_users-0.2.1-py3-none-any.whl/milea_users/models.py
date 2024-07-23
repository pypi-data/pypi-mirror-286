from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as BaseGroup
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from milea_notify.models import Setting
from milea_users.managers import UserManager


class Group(BaseGroup):
    class Meta:
        proxy = True
        verbose_name = _("group")
        verbose_name_plural = _("groups")


class User(AbstractUser):
    username = first_name = last_name = None
    email = models.EmailField(_('email address'), unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.profile.first_name, self.profile.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.profile.first_name

    def get_initials(self):
        """Return the short name for the user."""
        if hasattr(self, 'profile') and self.profile.first_name and self.profile.last_name:
            return self.profile.first_name[0] + self.profile.last_name[0]
        else:
            return self.email[0:2]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_staff and not hasattr(self, 'profile'):
            Profile(user=self).save()

    def __str__(self):
        if not hasattr(self, 'profile'):
            return self.email
        return '%s %s' % (self.profile.first_name, self.profile.last_name) if self.profile.last_name else self.email


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    def get_option(self, app_label, cls_name, option_field):
        """ Get the value from the option or give the default value from the model field """
        cls_name = cls_name.lower()
        cls = getattr(self, f'{app_label}_{cls_name}_option', None)
        if cls is None:
            return apps.get_model(f'{app_label}.{cls_name}')._meta.get_field(option_field).default
        else:
            return getattr(cls, option_field)

    def __str__(self):
        return f"{self.user}'s Profile"

    class Meta:
        verbose_name = _("User profile")
        verbose_name_plural = _("User profiles")
        default_permissions = ()
        permissions = [
            ("change_own_profile", "Can change own profile"),
            ("add_profile", "Can add all users profile"),
            ("change_profile", "Can change all users profile"),
            ("view_profile", "Can view all users profile"),
        ]


class MileaUserOption(models.Model):
    profile = models.OneToOneField('milea_users.Profile', on_delete=models.CASCADE, editable=False, related_name="%(app_label)s_%(class)s_option",)

    class Meta:
        abstract = True
        default_permissions = ()


@receiver(post_save, sender=User)
def create_notify_settings(sender, instance, created, **kwargs):
    if created:
        # Create default notification settings object
        Setting(user=instance).save()
