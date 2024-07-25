import inspect
import warnings

from django.contrib.auth.models import Group

from milea_notify.exceptions import NotifyRecipientError
from milea_notify.models import Notification
from milea_notify.tasks import send_email_async


class Notify():

    def __init__(self, title, content, user=None, group=None, is_important=False, url=None):
        self.user = user
        self.group = group
        self.title = title
        self.content = content
        self.is_important = is_important
        self.url = url

        # Add the notify function name to the instance
        try:
            stack = inspect.stack()
            self.func = stack[1].function
        except IndexError:
            self.func = None

    def __check_permission(self, user):
        """Check if user has gave the Permission for this Notification"""

        # Check user permission
        if not user.notify.has_permission(self.func):
            return False

        return True

    def __get_users(self):
        """Get the right recipients of this Notification based on the input"""

        users = []

        if self.group is None and self.user is None:
            raise NotifyRecipientError()

        if self.group is not None:
            try:
                group = Group.objects.get(name=self.group)
                users.extend(group.user_set.all())
            except Group.DoesNotExist:
                warnings.warn("Group '{}' does not exist. Notify not saved.".format(self.group), UserWarning)

        if self.user is not None and self.user not in users:
            users.append(self.user)

        return users

    def to_browser(self):
        """Creates a user notification right in the Browser"""

        users = self.__get_users()
        for user in users:

            if self.__check_permission(user):
                notify = Notification(
                    user=user,
                    title=self.title,
                    content=self.content,
                    is_important=self.is_important,
                    url=self.url
                )
                notify.save()

    def to_email(self):
        """Creates a user notification per email"""

        users = self.__get_users()
        for user in users:

            if self.__check_permission(user):
                send_email_async(
                    self.title,
                    self.content,
                    user.email
                )

    def to_email_async(self):
        """Creates a async user notification per email"""

        users = self.__get_users()
        for user in users:

            if self.__check_permission(user):
                send_email_async.delay(
                    self.title,
                    self.content,
                    user.email
                )
