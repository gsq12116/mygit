from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='标题')
    type = models.CharField(max_length=10, verbose_name='种类', null=True)
    abstract = models.CharField(max_length=255, default='文章暂无简介', verbose_name='摘要')
    image = models.ImageField(upload_to='upload', null=True, verbose_name='图片')
    content = models.TextField(verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创始时间')
    operate_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    class Meta:
        db_table = 'articles'
