# Generated by Django 2.1.4 on 2019-01-21 05:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_apps', '0002_auto_20190121_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='related_post',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
