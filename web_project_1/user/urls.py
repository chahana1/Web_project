from django.urls import path,include
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

urlpatterns = [
    path('signup/', views.signup,name="signup"),
    # 장고 로그인 이용
    # path('login/', views.isLogin,name="login"),
    path('login/', auth_views.LoginView.as_view(template_name="user/login.html"),name="login"),
    path('logout/', auth_views.LogoutView.as_view(),name="logout"),
    path('profile/', views.profile, name="profile"),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name = "user/password_change.html", success_url = reverse_lazy("main")), name="password_change"),
    
    # 클래스 뷰
    path("password_reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

