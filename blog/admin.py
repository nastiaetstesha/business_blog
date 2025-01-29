from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    raw_id_fields = ('likes',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text',)
    raw_id_fields = ('post', 'author')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', )