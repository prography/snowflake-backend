# Generated by Django 3.0.7 on 2020-11-22 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20201003_1601'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='num_of_likes',
            new_name='likes_count',
        ),
    ]
