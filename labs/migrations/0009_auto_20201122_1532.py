# Generated by Django 3.0.7 on 2020-11-22 06:32

from django.db import migrations, models
import labs.models


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0008_auto_20201012_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='welcomecard',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=labs.models.create_path),
        ),
    ]
