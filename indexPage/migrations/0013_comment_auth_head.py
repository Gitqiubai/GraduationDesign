# Generated by Django 2.1.5 on 2019-05-06 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0012_auto_20190429_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='auth_head',
            field=models.ImageField(default='/static/usermess/images/head.jpg', max_length=200, upload_to='upload/head/', verbose_name='评论者头像'),
        ),
    ]
