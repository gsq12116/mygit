from django.contrib import admin

# Register your models here.
from my_boke.models import Article


class ArticleAdmin(admin.ModelAdmin):
    # 修改管理后台展示列表的字段
    list_display = ['id', 'title', 'type', 'abstract', 'image', 'content']
    # 过滤
    list_filter = ['type']


admin.site.register(Article, ArticleAdmin)