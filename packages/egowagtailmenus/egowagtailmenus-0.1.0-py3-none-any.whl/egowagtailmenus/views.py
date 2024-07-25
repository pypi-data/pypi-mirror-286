import json

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.admin.panels import FieldPanel
from wagtail.models import Locale, Page
from wagtail.snippets.views.snippets import SnippetViewSet

from egowagtailmenus.models import Menu, MenuItem
from egowagtailmenus.permissions import IsSuperUser
from egowagtailmenus.serializers import CreateMenuItemSerializer, MenuAdminSerializer, MoveMenuItemSerializer


class MenuViewSet(SnippetViewSet):
    model = Menu
    icon = "bars"
    menu_label = _("Menus")
    base_url_path = "menus"
    add_to_admin_menu = True
    list_display = ["name", "slug", "site"]
    list_filter = ["site"]

    edit_template_name = "egowagtailmenus/admin/edit.html"

    panels = [FieldPanel("name"), FieldPanel("site")]


class MenuAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        try:
            menu = Menu.objects.get(pk=kwargs["menu_id"])
            if not menu.root:
                menu.root = MenuItem.add_root(title=f"{menu.name} Root")
                menu.save()
            return Response(
                MenuAdminSerializer(menu).data,
                status=status.HTTP_200_OK,
            )
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MoveItemAPIView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = MoveMenuItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            menu_item = serializer.validated_data["item"]
            parent = serializer.validated_data["parent"]
            position = serializer.validated_data["position"]

            # Based on wagtail's page move wagtail.admin.views.pages.ordering.set_page_position
            position_item = None

            try:
                position_item = parent.get_children()[int(position)]
            except IndexError:
                pass

            if position_item:
                menu_item.move(position_item, pos="left")
            else:
                menu_item.move(parent, pos="last-child")

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateItemAPIView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        serializer = CreateMenuItemSerializer(data=request.data)
        if serializer.is_valid():
            parent = serializer.validated_data.get("parent")
            item_type = serializer.validated_data.get("item_type")
            title = serializer.validated_data.get("title", None)
            page = serializer.validated_data.get("page", None)
            url = serializer.validated_data.get("url", None)
            target = serializer.validated_data.get("target", MenuItem._meta.get_field("target").get_default())

            parent.add_child(
                item_type=item_type,
                title=title,
                page=page,
                url=url,
                target=target,
            )
            return Response(
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateMenuItemAPIView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        data = request.data
        item_id = data.get("id", None)
        if item_id:
            try:
                payload = {k: v for k, v in data.items() if k != "id"}
                menu_item = MenuItem.objects.get(pk=item_id)

                for k, v in payload.items():
                    if k == 'page':
                        v = Page.objects.filter(pk=v).first()
                    setattr(menu_item, k, v)

                menu_item.save()

                return Response(status=status.HTTP_200_OK)
            except MenuItem.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "id is required"}, status=status.HTTP_400_BAD_REQUEST)


class DeleteMenuItemAPIView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, id, *args, **kwargs):
        try:
            menu_item = MenuItem.objects.get(pk=id)
            menu_item.delete()
            return Response(status=status.HTTP_200_OK)
        except MenuItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PageListAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        lang_code = request.GET.get("l", Locale.get_default().language_code)
        locale = Locale.objects.get(language_code=lang_code)

        locale_root = Page.objects.filter(locale=locale).exclude(pk=1).only("url_path").first().url_path

        pages = Page.objects.filter(locale=locale).exclude(pk=1).only("pk", "title", "url_path").order_by("path")

        results = []

        for page in pages:
            results.append(
                {
                    "id": page.pk,
                    "title": page.title,
                    "url": f"/{locale.language_code}" + page.url_path.replace(locale_root, "/"),
                    "depth": page.depth - 2,
                }
            )

        return Response(
            results,
            status=status.HTTP_200_OK,
        )


class MenuExportAPIView(APIView):
    permission_classes = [IsSuperUser]

    def get(self, request, *args, **kwargs):
        try:
            menu = Menu.objects.get(pk=kwargs["menu_id"])

            return Response(
                MenuAdminSerializer(menu).data,
                status=status.HTTP_200_OK,
            )
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MenuImportAPIView(APIView):
    permission_classes = [IsSuperUser]

    def post(self, request, *args, **kwargs):
        try:
            menu = Menu.objects.get(pk=kwargs["menu_id"])

            items = json.loads(request.data.get("content"))

            descendants = menu.root.get_descendants()
            for descendant in descendants:
                descendant.delete()

            self.create_items(menu.root, items)

            return Response(
                status=status.HTTP_200_OK,
            )
        except json.decoder.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create_items(self, parent, items):
        for item in items:
            page_id = Page.objects.filter(pk=item["page_id"]).first().pk if item["page_id"] else None
            new_item = parent.add_child(
                item_type=item["item_type"],
                title=item["title"],
                slug=item["slug"],
                url=item["url"],
                page_id=page_id,
                target=item["target"],
                description=item["description"],
                extra_class=item["extra_class"],
            )

            self.create_items(new_item, item["children"])
