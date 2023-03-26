from django.contrib import admin
from .models import Todo

# 모델을 어드민 사이트에서 관리할 수 있도록 등록
admin.site.register(Todo)
