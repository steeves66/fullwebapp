# Generated by Django 5.1.4 on 2024-12-10 16:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoverImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_link', models.URLField()),
                ('blog', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='blog_ci', to='blog.blog')),
            ],
        ),
    ]