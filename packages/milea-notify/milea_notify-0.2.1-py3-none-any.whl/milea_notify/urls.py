from django.urls import path

from milea_notify import views

app_name = "milea_notify"

urlpatterns = [
    path("action/mark_as_read/<int:notification_id>", views.mark_as_read, name="mark_as_read"),
]
