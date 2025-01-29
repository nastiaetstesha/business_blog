# Generated by Django 5.1.5 on 2025-01-29 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_alter_comment_published_at_alter_post_published_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='published_at',
            field=models.DateTimeField(verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=20, unique=True, verbose_name='Тег'),
        ),
    ]
