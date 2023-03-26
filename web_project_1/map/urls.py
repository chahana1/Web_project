from django.urls import path
from .import views
# from board.views import list


urlpatterns = [
    path("", views.maps, name="maps"),
]
