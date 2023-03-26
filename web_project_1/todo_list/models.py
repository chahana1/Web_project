from django.db import models
from user.models import User

# Create your models here.


class Todo(models.Model):
    # 필드 정의(필드 타입)
    title = models.CharField(max_length=50)
    user = models.ForeignKey(User, verbose_name="사용자",
                             on_delete=models.CASCADE)
    description = models.TextField()  # textarea
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    important = models.BooleanField(default=False)
    start_date = models.DateTimeField(verbose_name="시작일시")
    end_date = models.DateTimeField(verbose_name="종료일시")
    vol_id = models.IntegerField(default=False,null=True,blank=True)

    def __str__(self) -> str:
        return self.title
