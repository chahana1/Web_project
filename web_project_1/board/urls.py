from django.urls import path
from .import views
# from board.views import list


urlpatterns = [
    # board
    path("index/", views.home, name="board_index"),
    path("detail/<int:pk>/", views.detail, name="board_detail"),
    path("write", views.update, name="board_write"),
    path("delete/<int:pk>/", views.remove, name="board_remove"),
    path("edit/<int:pk>/", views.edit, name="board_edit"),



    # 댓글
    path("<int:post_pk>/comment/create/", views.comment_create,
         name="comment_create"),

    path("<int:post_pk>/comment/<int:comment_pk>/remove/",
         views.comment_remove, name="comment_remove"),
    path("comment/<int:post_pk>/update/<int:comment_pk>",
         views.comment_update, name="comment_update"),
    # 추천수
    path('like/<int:post_id>/', views.vote_question, name="vote_question"),



    # 대댓글
    path("comment/<int:comment_pk>/create/<int:post_pk>",
         views.comment_write, name="comment_write"),

]
