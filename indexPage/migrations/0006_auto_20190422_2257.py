# Generated by Django 2.1.5 on 2019-04-22 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0005_auto_20190422_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content_verify',
            field=models.BooleanField(default=0, verbose_name='审核状态[✔通过]'),
        ),
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.BooleanField(default=0, verbose_name='找回状态审核状态[✔已找回]'),
        ),
    ]
