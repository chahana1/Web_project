from django.urls import path
from .import views
# from board.views import list


urlpatterns = [
    path("", views.index, name="todo_list"),
    path("add_event/", views.add_event, name="add_event"),
    path("<int:pk>/", views.event_detail, name="event_detail"),
    path("<int:pk>/edit/", views.event_edit, name="event_edit"),
    path("post/delete/<int:pk>/", views.event_delete, name="event_delete"),
]
