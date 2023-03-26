from django.db import models
from user.models import User
from django.urls import reverse
# from imagekit.models import ImageSpecField
# from imagekit.processors import Thumbnail
# from imagekit.processors import ResizeToFill
# Create your models here.


class Care(models.Model):
    title = models.CharField(max_length=30)
    place = models.CharField(max_length=15)
    content = models.TextField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, null=True, verbose_name="이미지")
    updated_at = models.DateTimeField(auto_now=True)
    best = models.ManyToManyField(
        User, related_name="best", verbose_name="추천수")
    view_count = models.IntegerField(default=0)
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자")
    comment_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("board_detail", args=[self.pk])

    def get_previous(self):
        return self.get_previous_by_created_at()

    def get_next(self):
        return self.get_next_by_created_at()


class CareCount(models.Model):
    ip = models.CharField(max_length=30)
    question = models.ForeignKey(Care, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.ip


class Comment(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자")
    contents = models.TextField(verbose_name="내용")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성날짜")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="수정날짜")
    post = models.ForeignKey(
        Care, on_delete=models.CASCADE, null=True, blank=True)
    comment_count = models.IntegerField(default=0)


class ReComment(models.Model):
    writer = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="작성자")
    content = models.TextField(verbose_name='대댓글')
    created_at = models.DateTimeField(verbose_name='작성날짜', auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name='수정날짜', auto_now=True)
    answer = models.ForeignKey(
        Comment, on_delete=models.CASCADE, null=True, blank=True)
