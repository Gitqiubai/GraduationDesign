# Generated by Django 2.1.5 on 2019-05-24 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userlogin', '0008_auto_20190427_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message_table',
            name='headImage',
            field=models.ImageField(default='upload/head/admin_15587245218983266.jpg', max_length=200, upload_to='upload/head/', verbose_name='头像'),
        ),
    ]
