from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

# apps.py
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        import accounts.signals  # Replace with your actual app name
