from django import template
from django.conf import settings as django_settings
from django.template import TemplateDoesNotExist
from django.template.loader import select_template
from django.utils.safestring import mark_safe
from wagtail.models import Locale

from egowagtailmenus import settings as default_ego_wagtail_menu_settings
from egowagtailmenus.models import Menu

register = template.Library()

if hasattr(django_settings, "egowagtailmenus"):
    menu_settings = django_settings.egowagtailmenus | default_ego_wagtail_menu_settings.egowagtailmenus
else:
    menu_settings = default_ego_wagtail_menu_settings.egowagtailmenus


@register.simple_tag(takes_context=True)
def render_menu(context, slug, template=None):
    context = context.flatten()
    try:
        folder = menu_settings.get("DEFAULT_FOLDER")
        template_names_list = [
            f"{folder}/{slug}.html",
            f"{folder}/menu.html",
        ]
        menu = Menu.objects.get(slug=slug, locale=Locale.get_active())
        if template:
            template_names_list.insert(0, template)

        context["menu"] = menu.root
        return select_template(template_names_list).render(context)
    except Menu.DoesNotExist:
        return mark_safe(f"<!-- Menu {slug} does not exist -->")
    except TemplateDoesNotExist:
        return ""


@register.simple_tag(takes_context=True)
def render_menu_item(context, item, template=None):
    context = context.flatten()
    try:
        folder = menu_settings.get("DEFAULT_FOLDER")
        template_names_list = [
            f"{folder}/{item.get_root().menu.slug}/level_{item.depth}/menu_item_{item.item_type}.html",
            f"{folder}/{item.get_root().menu.slug}/level_{item.depth}/menu_item.html",
            f"{folder}/{item.get_root().menu.slug}/menu_item_{item.item_type}.html",
            f"{folder}/{item.get_root().menu.slug}/menu_item.html",
            f"{folder}/level_{item.depth}/menu_item_{item.item_type}.html",
            f"{folder}/level_{item.depth}/menu_item.html",
            f"{folder}/menu_item_{item.item_type}.html",
            f"{folder}/menu_item.html",
        ]

        if template:
            template_names_list.insert(0, template)

        context["item"] = item
        return select_template(template_names_list).render(context)
    except TemplateDoesNotExist:
        return ""


@register.simple_tag
def render_item_children(item, template=None):
    try:
        if item.get_children():
            folder = menu_settings.get("DEFAULT_FOLDER")
            template_names_list = [
                f"{folder}/{item.get_root().menu.slug}/level_{item.depth}/sub_menu.html",
                f"{folder}/{item.get_root().menu.slug}/sub_menu.html",
                f"{folder}/level_{item.depth}/sub_menu.html",
                f"{folder}/sub_menu.html",
            ]

            if template:
                template_names_list.insert(0, template)

            return select_template(template_names_list).render({"children": item.get_children()})
        return ""
    except TemplateDoesNotExist:
        return ""
