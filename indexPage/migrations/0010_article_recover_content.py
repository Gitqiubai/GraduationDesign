# Generated by Django 2.1.5 on 2019-04-28 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0009_auto_20190428_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='recover_content',
            field=models.TextField(default='找回了东西但是什么都没有说呢。', verbose_name='找回/归还后的话'),
        ),
    ]
