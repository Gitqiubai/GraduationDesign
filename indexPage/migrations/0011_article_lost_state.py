# Generated by Django 2.1.5 on 2019-04-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0010_article_recover_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='lost_state',
            field=models.BooleanField(default=0, verbose_name='类型[0丢失/1拾取]'),
        ),
    ]
