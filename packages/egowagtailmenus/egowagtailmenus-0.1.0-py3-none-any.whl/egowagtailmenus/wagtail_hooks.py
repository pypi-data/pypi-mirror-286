from django.urls import path
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.snippets.models import register_snippet

from egowagtailmenus.views import (
    CreateItemAPIView,
    DeleteMenuItemAPIView,
    MenuAPIView,
    MenuExportAPIView,
    MenuImportAPIView,
    MenuViewSet,
    MoveItemAPIView,
    PageListAPIView,
    UpdateMenuItemAPIView,
)

register_snippet(MenuViewSet)


@hooks.register("register_admin_urls")
def register_menus_api_urls():
    return [
        path("menus/api/menu/<int:menu_id>/", MenuAPIView.as_view(), name="menu"),
        path("menus/api/move_item/", MoveItemAPIView.as_view(), name="move_item"),
        path("menus/api/create_item/", CreateItemAPIView.as_view(), name="create_item"),
        path("menus/api/update_item/", UpdateMenuItemAPIView.as_view(), name="update_item"),
        path("menus/api/delete_item/<int:id>/", DeleteMenuItemAPIView.as_view(), name="delete_item"),
        path("menus/api/menu/export/<int:menu_id>/", MenuExportAPIView.as_view(), name="menu_export"),
        path("menus/api/menu/import/<int:menu_id>/", MenuImportAPIView.as_view(), name="menu_import"),
        path("menus/api/pages/", PageListAPIView.as_view(), name="pages"),
    ]
