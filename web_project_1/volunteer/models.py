import datetime
from django.utils import timezone

from django.db import models
from user.models import User

# Create your models here.


class Organization(models.Model):
    org_name = models.CharField(max_length=15, verbose_name="단체 및 시설 이름")
    addr = models.CharField(max_length=100, verbose_name="주소")
    director = models.CharField(max_length=15, verbose_name="담당자")
    phone_num = models.CharField(max_length=15, verbose_name="담당자 연락처")

    def __str__(self) -> str:
        return "%s" % (self.org_name)


class Volunteer(models.Model):
    title = models.CharField(max_length=30, verbose_name="제목")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name="봉사단체")
    content = models.TextField(null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")
    image = models.ImageField(blank=True, null=True, verbose_name="이미지")
    updated_at = models.DateTimeField(auto_now=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    sign_vol = models.ManyToManyField(User, related_name='sign_up', verbose_name='신청')