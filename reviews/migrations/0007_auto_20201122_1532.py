# Generated by Django 3.0.7 on 2020-11-22 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_review_num_of_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='num_of_likes',
            new_name='likes_count',
        ),
    ]
