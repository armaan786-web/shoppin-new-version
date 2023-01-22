from django.apps import AppConfig


class ShoppingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopping_app'
    def ready(self):
        import shopping_app.signal
