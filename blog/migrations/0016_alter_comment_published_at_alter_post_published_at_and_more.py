# Generated by Django 5.1.5 on 2025-01-29 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0015_alter_comment_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='published_at',
            field=models.DateTimeField(db_index=True, verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='post',
            name='published_at',
            field=models.DateTimeField(db_index=True, verbose_name='Дата и время публикации'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(db_index=True, max_length=20, unique=True, verbose_name='Тег'),
        ),
    ]
