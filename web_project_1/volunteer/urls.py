from django.urls import path
from . import views
# from board.views import list


urlpatterns = [
    path("", views.vol_index, name="vol_index"),
    path("<int:pk>", views.vol_detail, name="vol_detail"),
    path("<int:pk>/sign", views.sign_vol, name="sign_vol"),
    path("<int:pk>/add_cal", views.add_cal, name="add_cal"),
    path("create_vol", views.create_vol, name="create_vol"),
    path("create_org", views.create_org, name="create_org"),
]
