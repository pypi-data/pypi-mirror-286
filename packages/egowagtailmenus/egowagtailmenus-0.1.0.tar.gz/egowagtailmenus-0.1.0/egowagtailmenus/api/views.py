from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from wagtail.models import Locale, Site

from egowagtailmenus.models import Menu, MenuItem
from egowagtailmenus.serializers import MenuListSerializer, MenuSerializer


class MenuAPIView(APIView):

    def get(self, request, *args, **kwargs):

        if "site" in request.GET:
            if ":" in request.GET["site"]:
                (hostname, port) = request.GET["site"].split(":", 1)
                query = {
                    "hostname": hostname,
                    "port": port,
                }
            else:
                query = {
                    "hostname": request.GET["site"],
                }

            try:
                site = Site.objects.get(**query)
            except Site.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

        else:
            # Otherwise, find the site from the request
            site = Site.find_for_request(request)

        locale = Locale.get_default()
        if 'locale' in request.GET:
            try:
                locale = Locale.objects.get(language_code=request.GET['locale'])
            except Locale.DoesNotExist:
                pass

        try:
            menu = Menu.objects.get(site=site, locale=locale, slug=request.GET.get('slug'))
            return Response(
                MenuSerializer(menu).data,
                status=status.HTTP_200_OK,
            )
        except Menu.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
