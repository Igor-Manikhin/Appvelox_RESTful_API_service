# Generated by Django 3.0.8 on 2020-07-14 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0004_auto_20200714_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resizeimages',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
    ]
