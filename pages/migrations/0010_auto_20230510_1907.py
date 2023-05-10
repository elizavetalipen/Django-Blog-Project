# Generated by Django 3.2.5 on 2023-05-10 16:07

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0009_auto_20230507_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cathegory',
            name='cathegory_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='cath_image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='post_image'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='cover_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, verbose_name='cover'),
        ),
    ]