# Generated by Django 3.0.7 on 2020-07-10 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20200710_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resizeimages',
            name='save_format',
            field=models.CharField(max_length=4),
        ),
    ]
