from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'ctrp3_py3.users'
    verbose_name = "Users"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
