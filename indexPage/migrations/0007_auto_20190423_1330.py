# Generated by Django 2.1.5 on 2019-04-23 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0006_auto_20190422_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content_verify',
            field=models.ImageField(default=0, upload_to='', verbose_name='审核状态[0未审核 1通过 2不通过]'),
        ),
    ]
