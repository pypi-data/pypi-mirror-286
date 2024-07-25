from rest_framework import serializers
from wagtail.models import Page

from egowagtailmenus.models import Menu, MenuItem, MenuItemTypeChoices


class MenuListSerializer(serializers.ModelSerializer):
    locale = serializers.CharField(source="locale.language_code")

    class Meta:
        model = Menu
        fields = ("id", "name", "slug", "locale")


class MenuSerializer(serializers.ModelSerializer):
    root = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    lang_code = serializers.CharField(source="locale.language_code")

    def get_id(self, obj):
        return obj.root.pk

    def get_root(self, obj):
        return MenuItemSerializer(obj.root.get_children(), many=True).data

    class Meta:
        model = Menu
        fields = (
            "id",
            "root",
            "lang_code",
        )


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class MoveMenuItemSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    parent = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    position = serializers.IntegerField(default=0)


class MenuItemSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, source="get_children")

    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        if obj.item_type == MenuItemTypeChoices.EXTERNAL_LINK:
            return obj.url

        if obj.item_type == MenuItemTypeChoices.INTERNAL_LINK:
            url = obj.page.get_url().replace(obj.page.get_site().root_url, '')
            return url[:-1] if url.endswith("/") else url

    class Meta:
        model = MenuItem
        fields = (
            "id",
            "item_type",
            "title",
            "slug",
            "url",
            "target",
            "description",
            "extra_class",
            "children",
        )


class MenuAdminSerializer(serializers.ModelSerializer):
    root = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    lang_code = serializers.CharField(source="locale.language_code")

    def get_id(self, obj):
        return obj.root.pk

    def get_root(self, obj):
        return MenuItemAdminSerializer(obj.root.get_children(), many=True).data

    class Meta:
        model = Menu
        fields = (
            "id",
            "root",
            "lang_code",
        )


class MenuItemAdminSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True, source="get_children")

    class Meta:
        model = MenuItem
        fields = (
            "id",
            "item_type",
            "title",
            "slug",
            "url",
            "page_id",
            "target",
            "description",
            "extra_class",
            "children",
        )


class CreateMenuItemSerializer(serializers.Serializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    item_type = serializers.ChoiceField(choices=MenuItemTypeChoices.choices)
    title = serializers.CharField(required=False)
    page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all(), required=False)
    url = serializers.URLField(required=False)
    target = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    extra_class = serializers.CharField(required=False)
