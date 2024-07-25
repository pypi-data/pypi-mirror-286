from django.db import models
from django.utils.text import slugify as _slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from treebeard.mp_tree import MP_Node
from wagtail.models import Site, TranslatableMixin
from wagtail.snippets.models import register_snippet


class MenuItemTypeChoices(models.TextChoices):
    ROOT = "root", _("Root")
    SECTION = "section", _("Section")
    SEPARATOR = "separator", _("Separator")
    TEXT = "text", _("Text")
    INTERNAL_LINK = "internal_link", _("Internal Link")
    EXTERNAL_LINK = "external_link", _("External Link")


class MenuItemTargetChoices(models.TextChoices):
    SELF = "_self", _("Same Window")
    BLANK = "_blank", _("New Window")


class MenuItem(MP_Node):
    item_type = models.CharField(max_length=20, choices=MenuItemTypeChoices.choices, default=MenuItemTypeChoices.ROOT)

    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Title"))
    slug = AutoSlugField(
        populate_from="title",
        separator="_",
        overwrite=True,
        allow_duplicates=True,
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Slug"),
    )
    page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+", verbose_name=_("Page")
    )
    url = models.URLField(null=True, blank=True, verbose_name="URL")
    target = models.CharField(
        max_length=10,
        choices=MenuItemTargetChoices.choices,
        default=MenuItemTargetChoices.SELF,
        verbose_name=_("Target"),
    )
    description = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Description"))
    extra_class = models.CharField(max_length=200, null=True, blank=True, verbose_name=_("Extra class"))

    @property
    def get_url(self):
        if self.item_type == MenuItemTypeChoices.INTERNAL_LINK:
            return self.page.get_url()

        if self.item_type == MenuItemTypeChoices.EXTERNAL_LINK:
            return self.url

        return "#"

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")


# @register_snippet
class Menu(TranslatableMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from="name",
        separator="_",
        overwrite=True,
        allow_duplicates=True,
        editable=False,
    )
    root = models.OneToOneField(MenuItem, null=True, blank=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)

    translatable_fields = []
    exclude_fields_in_copy = ["root"]

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.root:
            self.root.delete()
        super(Menu, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # sync name, slug and site accross all translations
        if self.pk:
            self.slug = _slugify(self.name)
            super(Menu, self).save(*args, **kwargs)
            for translation in self.get_translations():
                if translation.name != self.name or translation.site != self.site:
                    translation.name = self.name
                    translation.site = self.site
                    translation.save()
        else:
            super(Menu, self).save(*args, **kwargs)

    class Meta(TranslatableMixin.Meta):
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")
