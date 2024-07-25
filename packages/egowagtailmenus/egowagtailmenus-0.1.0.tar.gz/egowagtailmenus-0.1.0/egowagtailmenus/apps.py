from django.apps import AppConfig


class EgoWagtailMenusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'egowagtailmenus'

    def ready(self) -> None:

        from wagtail.models.reference_index import ReferenceIndex

        from .models import Menu, MenuItem

        ReferenceIndex.register_model(Menu)
        ReferenceIndex.register_model(MenuItem)
