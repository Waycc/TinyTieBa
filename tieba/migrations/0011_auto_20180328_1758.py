# Generated by Django 2.0.1 on 2018-03-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tieba', '0010_auto_20180328_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='role',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='role',
        ),
        migrations.AddField(
            model_name='role',
            name='permission',
            field=models.ManyToManyField(to='tieba.Permission'),
        ),
        migrations.AlterField(
            model_name='permission',
            name='permission',
            field=models.CharField(max_length=500),
        ),
    ]
