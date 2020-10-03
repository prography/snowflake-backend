# Generated by Django 3.0.7 on 2020-10-03 06:31

from django.db import migrations, models
import labs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WelcomeCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('tag_txt', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('button_src', models.URLField(max_length=2000)),
                ('button_txt', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to=labs.models.create_path)),
                ('category', models.CharField(choices=[('NONE', '지정안됨'), ('SUTRA', '눈송수트라'), ('ATOZ', 'A to Z'), ('SONG_DOCTOR', '송박사의 연구소')], default='NONE', max_length=30)),
                ('sequence', models.IntegerField(default=-1)),
                ('status', models.CharField(choices=[('DEL', 'Deleted'), ('DRAFT', 'Draft'), ('PUB', 'Published')], default='DRAFT', max_length=5)),
            ],
        ),
    ]