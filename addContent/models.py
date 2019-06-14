from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.


class articles(models.Model):

    article_id = models.IntegerField(primary_key=True,auto_created=True,verbose_name='帖子id')
    title = models.CharField(max_length=100,verbose_name='标题')
    #content = models.TextField(verbose_name='内容')
    content =RichTextUploadingField(verbose_name='内容')
    uid = models.CharField(max_length=100,verbose_name='发帖人')
    data = models.DateTimeField(auto_now=True,verbose_name='发帖时间')
    addr = models.CharField(max_length=200,default='南宁学院',verbose_name='遗失/拾取地点')
    item = models.CharField(max_length=20,default='未知',verbose_name='物品名')
    lostdate = models.CharField(max_length=100,default='未知',verbose_name='遗失/拾取时间')


    class Meta:
        verbose_name='帖子'
        verbose_name_plural=verbose_name

    def __unicode__(self):

        return self.title
