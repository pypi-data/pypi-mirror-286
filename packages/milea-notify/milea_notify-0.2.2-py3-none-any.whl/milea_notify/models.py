from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from milea_base.utils import MILEA_VARS


class Notification(models.Model):
    """
    Stores a single notification entry, related to user model.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name=_("title"))
    content = models.TextField(verbose_name=_("content"))
    is_read = models.BooleanField(default=False, db_index=True, verbose_name=_("read"))
    is_important = models.BooleanField(default=False, verbose_name=_("important"))
    url = models.URLField(max_length=200, blank=True, null=True, verbose_name=_("link"))
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_("created at"))

    class Meta:
        default_permissions = ()


class Setting(models.Model):
    """
    Notification settings for User
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notify')
    permissions = models.JSONField(default=dict, blank=True)

    def has_permission(self, func) -> bool:
        for key, value in self.permissions.items():
            if key == func and value is True:
                return True
            elif key == func and value is False:
                return False
        return MILEA_VARS['milea_notify']['AUTO_ENABLED']  # Default value

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ['user']
        verbose_name = _("Notification setting")
        verbose_name_plural = _("Notification settings")
        default_permissions = ()
        permissions = [
            ("change_own_settings", "Can change own setting"),
            ("add_setting", "Can add all users settings"),
            ("change_setting", "Can change all users settings"),
            ("view_setting", "Can view all users settings"),
        ]
