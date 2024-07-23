from django.contrib import admin

from milea_notify.decorators import registered_milea_notify_functions
from milea_notify.forms import SettingForm
from milea_notify.models import Setting


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):

    form = SettingForm
    list_select_related = ('user',)

    def get_form(self, request, obj=None, change=False, **kwargs):
        return SettingForm

    # Allow user to edit own notification settings
    def has_change_permission(self, request, obj=None):
        opts = self.opts
        has_perm = request.user.has_perm("%s.%s" % (opts.app_label, "change_own_settings"))
        if obj and obj.user == request.user and has_perm:
            return True
        return super().has_view_permission(request, obj)

    def get_fieldsets(self, request, obj=None):
        fieldsets = ()

        app_functions = {}
        for app, func, label in registered_milea_notify_functions:
            if app not in app_functions:
                app_functions[app] = []
            app_functions[app].append(func)

        for app, funcs in app_functions.items():
            fieldsets += (
                (app, {
                    'classes': ('mt-3 col-lg-4',),
                    'fields': tuple(funcs),
                }),
            )

        fieldsets += (
            (None, {
                'fields': ('user',),
            }),
        )

        return fieldsets
