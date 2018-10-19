from django.db import models

# Create your models here.


class HeroCategory(models.Model):

    CATEGORY_TYPE = (
        (1, '战士'),
        (2, '法师'),
        (3, '射手'),
        (4, '刺客'),
        (5, '坦克'),
        (6, '辅助'),
    )
    category_type = models.IntegerField(choices=CATEGORY_TYPE, help_text='类目级别', verbose_name='类目级别')

    class Meta:
        db_table = 'hero_category'


class Hero(models.Model):
    h_name = models.CharField(max_length=30, unique=True, verbose_name='英雄名称', null=False)
    h_category = models.ManyToManyField(HeroCategory, verbose_name='英雄类别', null=True)
    h_dir = models.TextField(default='暂无', verbose_name='英雄描述')

    class Meta:
        db_table = 'hero'


class HeroCombo(models.Model):
    c_name = models.CharField(max_length=128, verbose_name='连招名', null=False)
    c_dir = models.TextField(default='暂无', verbose_name='连招描述')
    c_hero = models.ForeignKey(Hero, verbose_name='英雄', on_delete=models.CASCADE)

    class Meta:
        db_table = 'hero_combo'


class HeroSkill(models.Model):
    s_name = models.CharField(max_length=40, verbose_name='技能名', null=False)
    s_dir = models.TextField(verbose_name='技能描述', null=False)
    s_hero = models.ForeignKey(Hero, verbose_name='英雄', on_delete=models.CASCADE)

    class Meta:
        db_table = 'hero_skill'