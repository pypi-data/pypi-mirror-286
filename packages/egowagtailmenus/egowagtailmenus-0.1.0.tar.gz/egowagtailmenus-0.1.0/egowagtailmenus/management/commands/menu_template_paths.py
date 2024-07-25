from django.conf import settings as django_settings
from django.core.management.base import BaseCommand

from egowagtailmenus import settings as default_ego_wagtail_menu_settings

if hasattr(django_settings, "egowagtailmenus"):
    menu_settings = django_settings.egowagtailmenus | default_ego_wagtail_menu_settings.egowagtailmenus
else:
    menu_settings = default_ego_wagtail_menu_settings.egowagtailmenus


class Command(BaseCommand):
    help = "Show possible template paths."

    def handle(self, *args, **options):
        folder = menu_settings.get("DEFAULT_FOLDER")

        menu_template_names_list = [
            f"{folder}/menu.html",
            f"{folder}/<menu_slug>.html",
        ]

        self.stdout.write("")
        self.stdout.write("Menus:")
        for item in menu_template_names_list:
            self.stdout.write(f" - {item}")

        children_template_names_list = [
            f"{folder}/<menu_slug>/level_<depth>/sub_menu.html",
            f"{folder}/<menu_slug>/sub_menu.html",
            f"{folder}/level_<depth>/sub_menu.html",
            f"{folder}/sub_menu.html",
        ]

        self.stdout.write("")
        self.stdout.write("Sub Menus:")
        for item in children_template_names_list:
            self.stdout.write(f" - {item}")

        item_template_names_list = [
            f"{folder}/<menu_slug>/level_<depth>/menu_item_<item_type>.html",
            f"{folder}/<menu_slug>/level_<depth>/menu_item.html",
            f"{folder}/<menu_slug>/menu_item_<item_type>.html",
            f"{folder}/<menu_slug>/menu_item.html",
            f"{folder}/level_<depth>/menu_item_<item_type>.html",
            f"{folder}/level_<depth>/menu_item.html",
            f"{folder}/menu_item_<item_type>.html",
            f"{folder}/menu_item.html",
        ]

        self.stdout.write("")
        self.stdout.write("Menu Items:")
        for item in item_template_names_list:
            self.stdout.write(f" - {item}")

        self.stdout.write("")
        self.stdout.write("Item types:")
        self.stdout.write(" - section")
        self.stdout.write(" - separator")
        self.stdout.write(" - text")
        self.stdout.write(" - external_link")
        self.stdout.write(" - internal_link")
