from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.contrib.auth.models import AbstractBaseUser, AbstractUser, BaseUserManager, PermissionsMixin, UserManager

# AbstractUser
# AbstractBaseUser 상속
# username, first_name, last_name, email
# is_staff, is_active,  date_joined


# AbstractBaseUser
# password, last_login, is_active


# User 객체
# 속성 - username, password, email(필수요소가 아님), first_name, last_name


# 프로젝트에서 필요한 User
# email 필드 == id 개념 == username
# gender 필드(필수는 아님)
# password
# name 필수

class UserManger(BaseUserManager):
    def _create_user(self, email, password, name, gender=2, **extra_fields):
        """
        Create and save a user with the given email,password,name.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, name=name,
                          gender=gender, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, name, gender, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, name, gender, **extra_fields)

    def create_superuser(self, email, password, name, **extra_fields):
        """
        성별은 입력 필요없음
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User 생성 : AbstractUser 상속 or AbstractBaseUser 상속
    필드 추가 : email, gender, name

    권한 여부 추가
    """
    # null=True 지정하지 않으면 not null, + unique ==> pk 속성
    email = models.EmailField(verbose_name='이메일', max_length=255, unique=True)
    password = models.CharField(verbose_name="비밀번호", max_length=128)
    name = models.CharField(verbose_name="이름", max_length=64)

    GENDER_CHOICES = [
        (0, '남자'),
        (1, '여자'),
        (2, '비공개'),
    ]
    gender = models.SmallIntegerField(
        verbose_name="성별", choices=GENDER_CHOICES, default=2)

    is_staff = models.BooleanField(verbose_name="관리자여부", default=False)
    is_active = models.BooleanField(verbose_name="활성화여부", default=True)

    # CustomUser 를 기반으로 user 생성을 도와줄 매니저 클래스 등록
    objects = UserManger()  # User.objects.create_user() 생성

    # username(아이디)으로 사용할 필드 지정
    USERNAME_FIELD = 'email'

    # email, password 요소 외에 사용자 생성 시 꼭 받아야 하는 필드 작성
    REQUIRED_FIELDS = ['name']


class Profile(models.Model):
    """
    회원가입 시 무조건 같이 실행
    """
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="회원")
    image = models.ImageField(
        upload_to="profile/", default="profile/default.png", verbose_name="프로필이미지")
    pet_name = models.CharField(max_length=50, verbose_name="반려동물 이름")
    address = models.CharField(max_length=50, verbose_name="주소")
    birth = models.CharField(max_length=10, verbose_name="반려동물 생일")
    char = models.TextField(verbose_name="반려동물 특징")

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    def __str__(self) -> str:
        return "<%d %s %s>" % (self.pk, self.email, self.name)
