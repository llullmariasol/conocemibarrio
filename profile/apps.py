from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profile'

    def ready(self):
        import profile.signals  # noqa


# Next step is to connect the receivers in the ready() method of the app's configuration by
# importing the signals module. Open apps.py where we can include any application configuration for the users app.

# What we did is override the ready() method of the users app config to perform initialization task which
# is registering signals.
