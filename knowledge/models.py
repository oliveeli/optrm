from uuid import uuid4

from django.db import models
from django.db.models import Field
from django.db.models.query import QuerySet

import mptt
from mptt.fields import TreeForeignKey, TreeManyToManyField, TreeOneToOneField
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from django.contrib.auth.models import User,Group
from mdeditor.fields import MDTextField


    

class Category(MPTTModel):
    name = models.CharField(max_length=64)
    parent = TreeForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "文章分类"
        verbose_name_plural = "文章分类"


class Article(models.Model):
    title = models.CharField(max_length=128,default='')
    category = TreeForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=False, verbose_name="分类")
    content = MDTextField(verbose_name='内容',max_length=50)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    create_user = models.ForeignKey(User, related_name="createUser", null=True, blank=False, verbose_name="创建人",on_delete=models.SET_NULL)
    update_time = models.DateTimeField('最后更新时间', null=True, blank=True)
    update_user = models.ForeignKey(User, related_name="updateUser", null=True, blank=True, verbose_name="最后更新人", on_delete=models.SET_NULL)
    user_group = models.ManyToManyField(Group, blank=True, verbose_name="授权用户组")

    def user_group_list(self):
        return ', '.join([a.name for a in self.user_group.all()])

    class MPTTMeta:
        order_insertion_by = ("create_time",)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"