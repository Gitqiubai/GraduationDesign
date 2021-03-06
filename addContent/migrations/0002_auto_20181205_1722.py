# Generated by Django 2.1.3 on 2018-12-05 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addContent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articles',
            name='item',
            field=models.CharField(default='未知', max_length=20, verbose_name='物品名'),
        ),
        migrations.AddField(
            model_name='articles',
            name='lostdate',
            field=models.CharField(default='未知', max_length=100, verbose_name='遗失/拾取时间'),
        ),
        migrations.AlterField(
            model_name='articles',
            name='addr',
            field=models.CharField(default='南宁学院', max_length=200, verbose_name='遗失/拾取地点'),
        ),
    ]
