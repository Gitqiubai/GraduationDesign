from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime


# Create your models here.


class article(models.Model):

    article_id = models.IntegerField(primary_key=True,auto_created=True,verbose_name='帖子id')
    title = models.CharField(max_length=100,verbose_name='标题')
    #content = models.TextField(verbose_name='内容')
    content =RichTextUploadingField(verbose_name='内容')
    uid = models.CharField(max_length=100,verbose_name='发帖人')
    newsdate = models.DateTimeField(auto_now=True,verbose_name='发帖时间')
    releasedate = models.DateTimeField(default=datetime.now,verbose_name='发帖时间')
    addr = models.CharField(max_length=200,default='南宁学院',verbose_name='发生地点')
    item = models.CharField(max_length=20, default='未知', verbose_name='物品名')
    lostdate = models.CharField(max_length=100, default='未知', verbose_name='遗失/拾取时间')
    reply_num = models.IntegerField(default=0,verbose_name='回复数量')
    state = models.BooleanField(default=0,verbose_name="找回状态[✔已找回]")
    content_verify = models.IntegerField(default=0,verbose_name="审核状态[0未审核 1通过 2不通过]")
    recover_content = models.TextField(default='找回了东西但是什么都没有说呢。', verbose_name='找回/归还后的话')
    lost_type = models.BooleanField(default=0,verbose_name='类型[0丢失/1拾取]')

    class Meta:
        verbose_name='帖子'
        verbose_name_plural=verbose_name

    def __str__(self):

        return self.title

class comment(models.Model):

    f = models.ForeignKey('article',on_delete=models.CASCADE)
    #comment_id=models.IntegerField(primary_key=True,auto_created=True,verbose_name='评论ID')
    #comment_id=models.IntegerField(verbose_name='评论ID')
    #article_id=models.IntegerField(verbose_name='帖子id')
    comment_to = models.CharField(max_length=100,verbose_name='原帖作者')
    comment_article_title = models.CharField(max_length=100,verbose_name='原帖标题')
    comment_content=models.CharField(max_length=500,verbose_name='评论内容')
    comment_auth=models.CharField(max_length=100,verbose_name='评论作者')
    comment_date=models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    read = models.BooleanField(default=False,verbose_name='消息已读')
    auth_head =models.ImageField(upload_to='upload/head/',default='/static/usermess/images/head.jpg',max_length=200,verbose_name='评论者头像')
    auth_nickname = models.CharField(max_length=10,default='未设昵称',verbose_name='昵称')






    class Meta:
        verbose_name='评论内容'
        verbose_name_plural=verbose_name


    def __str__(self):
        return self.comment_content

class Notices(models.Model):

    Notices_content = models.TextField(max_length=150,default='风平浪静的一天,没有公告呢。',verbose_name='公告内容')
    Notices_date = models.DateTimeField(auto_now=True,verbose_name='公告时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural=verbose_name

    def __str__(self):
        return str(self.Notices_date)




