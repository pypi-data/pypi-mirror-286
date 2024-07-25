from django.urls import include, path

from egowagtailmenus.api import views

urlpatterns = [
    path("menu/", views.MenuAPIView.as_view()),
]
