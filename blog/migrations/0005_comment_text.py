# Generated by Django 5.0 on 2024-02-16 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment_post_comments_like_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default='jkfy'),
            preserve_default=False,
        ),
    ]
