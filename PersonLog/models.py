from django.db import models
from django.db.models.signals import pre_delete,post_init, post_save
from django.dispatch import receiver
import os

# Create your models here.

class User(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="用户ID") # verbose_name表示在后台admin显示的名字
    username = models.CharField(max_length=255, verbose_name="用户名")
    passwd = models.CharField(max_length=100, verbose_name="密码")
    
class Person(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="人员ID") # verbose_name表示在后台admin显示的名字
    name = models.CharField(max_length=255, verbose_name="姓名")
    age = models.SmallIntegerField(verbose_name="年龄", null=True)
    pic = models.ImageField(upload_to='images/person_img',max_length=255, null=True)


# 删除文件是随便删除本地存储,删除时
@receiver(pre_delete, sender=Person)
def delete(sender, instance, **kwargs):
    instance.pic.delete(False)

# 删除文件是随便删除本地存储，修改时
@receiver(post_init, sender=Person)
def file_path(sender, instance, **kwargs):
    instance._current_pic = instance.pic
@receiver(post_save, sender= Person)
def delete_old_image(sender, instance, **kwargs):
    if hasattr(instance, '_current_pic'):
        if instance._current_pic != instance.pic:
            instance._current_pic.delete(save=False)