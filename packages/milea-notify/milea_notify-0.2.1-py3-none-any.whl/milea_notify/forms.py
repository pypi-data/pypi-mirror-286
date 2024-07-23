from django import forms

from milea_base.utils import MILEA_VARS
from milea_notify.decorators import registered_milea_notify_functions
from milea_notify.models import Setting


class SettingForm(forms.ModelForm):

    class Meta:
        model = Setting
        exclude = ['permissions',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hide user field for existing instances
        if 'instance' in kwargs:
            self.fields['user'] = forms.IntegerField(widget=forms.HiddenInput())

        # Add checkboxes from registered notify functions
        for app, func, label in registered_milea_notify_functions:
            self.base_fields[func] = forms.BooleanField(label=label, required=False)
            self.fields[func] = forms.BooleanField(label=label, required=False)

        # Set initial values from json
        initial = self.instance.permissions if self.instance and hasattr(self.instance, 'permissions') else {}
        for field in self.fields:
            self.fields[field].initial = initial.get(field, MILEA_VARS['milea_notify']['AUTO_ENABLED'])  # Default value for undefined or new notifications

        print(self.errors)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.permissions = {}

        for app, func, value in registered_milea_notify_functions:
            if func in self.cleaned_data:
                instance.permissions[func] = self.cleaned_data[func]

        instance.save()
        return instance
