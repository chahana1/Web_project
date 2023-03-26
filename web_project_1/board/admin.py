from django.contrib import admin
from .models import Care, Comment
# Register your models here.


class CareAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다.


admin.site.register(Care, CareAdmin)
admin.site.register(Comment)


