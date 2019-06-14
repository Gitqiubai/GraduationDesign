# Generated by Django 2.1.5 on 2019-05-09 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indexPage', '0014_comment_auth_nickname'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Notices_content', models.TextField(max_length=150, verbose_name='公告内容')),
                ('Notices_release_date', models.DateTimeField(auto_now_add=True, verbose_name='发表时间')),
            ],
            options={
                'verbose_name': '公告',
                'verbose_name_plural': '公告',
            },
        ),
        migrations.AlterField(
            model_name='article',
            name='state',
            field=models.BooleanField(default=0, verbose_name='找回状态[✔已找回]'),
        ),
    ]