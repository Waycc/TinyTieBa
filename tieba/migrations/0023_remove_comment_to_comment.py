# Generated by Django 2.0.1 on 2018-03-29 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tieba', '0022_auto_20180330_0254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='to_comment',
        ),
    ]
