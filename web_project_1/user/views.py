from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserForm,RegisterForm
# from django.contrib.auth.models import User
from django.contrib import messages
from community.models import Post
from board.models import Care
from find.models import Find
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView,View
from .models import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import AuthenticationForm


def signup(request):
    """
    회원가입
    get - 비어 있는 UserForm
    post - 바인딩 된 UserForm
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserForm()
    return render(request,"user/signup.html",{"form":form})

def profile(request):
    profile_detail = get_object_or_404(Profile,id=request.user.id)
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES, instance=profile_detail)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("profile")
    else:
        form = RegisterForm(instance=profile_detail)
        count = Post.objects.filter(writer = request.user.id).count()
        count1 = Care.objects.filter(writer = request.user.id).count()
        count2 = Find.objects.filter(writer = request.user.id).count()


    return render(request, 'users/profile.html',{"form":form,"count":count,"count1":count1,"count2":count2})


# def isLogin(request):

#     if request.method == "POST":
#         # username, password 가져오기
#         username = request.POST['email']
#         password = request.POST['password']

#         print("para", username, password)

#         # db 확인(사용자의 입력값과 데이터베이스 내용과 확인)
#         user = authenticate(request, username=username, password=password)

#         # 세션에 정보 저장
#         if user is not None:
#             login(request, user)
#             return redirect("main")
#         else:
#             messages.error(request, "이메일과 비밀번호를 확인해 주세요")
#             return render(request,"user/login.html")           

#     return render(request,"user/login.html")


class UserPasswordResetView(PasswordResetView):
    # 이메일을 입력 할 수 있는 화면
    template_name = "user/password_reset_form.html"
    # 이메일이 존재하는 경우 그 다음 작업을 진행할 경로 지정
    success_url = reverse_lazy("password_reset_done")
    # 이메일로 전송 될 페이지 지정
    email_template_name ="user/password_reset_email.txt"
    def form_valid(self, form):
        # 사용자가 입력한 이메일이 실제 존재하는 지 확인 후 없으면 에러 메세지 전송
        # 존재한다면 유효성 검증
        if User.objects.filter(email=self.request.POST.get("email")).exists():
            return super().form_valid(form)
        else:
            messages.info(self.request, "이메일을 확인해 주세요")
            return redirect("password_reset")
class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "user/password_reset_done.html"
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "user/password_reset_confirm.html"
class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "user/password_reset_complete.html"