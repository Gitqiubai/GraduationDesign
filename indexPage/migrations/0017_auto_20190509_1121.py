# Generated by Django 2.1.5 on 2019-05-09 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0016_auto_20190509_1117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notices',
            name='Notices_release_date',
        ),
        migrations.AddField(
            model_name='notices',
            name='Notices_date',
            field=models.DateTimeField(auto_now=True, verbose_name='公告时间'),
        ),
    ]
