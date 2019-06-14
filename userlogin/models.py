from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class message_table(AbstractUser):

    nick_name = models.CharField(max_length=10,default='未设昵称',verbose_name='昵称')
    male = models.CharField(max_length=2,default='隐藏',verbose_name='性别')
    addr = models.CharField(max_length=30,default='',verbose_name='地址')
    about = models.CharField(max_length=200,default='',verbose_name='签名')
    headImage = models.ImageField(upload_to='upload/head/',default='upload/head/admin_15587245218983266.jpg',max_length=200,verbose_name='头像')
    QQ = models.CharField(max_length=200,default="无",verbose_name='QQ')
    WeChats = models.CharField(max_length=200,default='无',verbose_name='微信')

    class Meta:
        verbose_name='用户信息'
        verbose_name_plural=verbose_name

    def __unicode__(self):

        return self.username

