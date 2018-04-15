# Generated by Django 2.0.1 on 2018-04-04 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tieba', '0028_auto_20180403_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tieba',
            name='background_img',
            field=models.ImageField(default='default/background.jpg', null=True, upload_to='tieba/background'),
        ),
        migrations.AlterField(
            model_name='tieba',
            name='head_img',
            field=models.ImageField(default='default/tieba_head.jpg', null=True, upload_to='tieba/head/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='head_img',
            field=models.ImageField(default='default/head.jpg', null=True, upload_to='user/head/'),
        ),
    ]
