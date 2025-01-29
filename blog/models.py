from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class PostQuerySet(models.QuerySet):
    def year(self, year):
        return self.filter(published_at__year=year).order_by('published_at')

    def popular(self):
        return self.annotate(
            likes_count=models.Count('likes', distinct=True)
        ).order_by('-likes_count').only('id', 'title', 'text', 'slug', 'image', 'published_at', 'author')

    def fetch_with_comments_count(self):

        post_ids = list(self.values_list('id', flat=True))

        comments_count = (
            Comment.objects
            .filter(post_id__in=post_ids)
            .values('post_id')
            .annotate(comments_count=models.Count('id'))
        )

        count_for_id = {item['post_id']: item['comments_count'] for item in comments_count}

        for post in self:
            post.comments_count = count_for_id.get(post.id, 0)

        return self


class TagQuerySet(models.QuerySet):
    def popular(self):
        return self.annotate(
            posts_count=models.Count('posts', distinct=True)
        ).order_by('-posts_count').only('id', 'title')


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    text = models.TextField('Текст')
    slug = models.SlugField('Название в виде url', max_length=200)
    image = models.ImageField('Картинка', blank=True, null=True)
    published_at = models.DateTimeField('Дата и время публикации')

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        limit_choices_to={'is_staff': True}
    )
    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        verbose_name='Кто лайкнул',
        blank=True
    )
    tags = models.ManyToManyField(
        'Tag',
        related_name='posts',
        verbose_name='Теги'
    )

    objects = PostQuerySet.as_manager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args={'slug': self.slug})

    class Meta:
        ordering = ['-published_at']
        verbose_name = 'пост'
        verbose_name_plural = 'посты'


class Tag(models.Model):
    title = models.CharField('Тег', max_length=20, unique=True)

    objects = TagQuerySet.as_manager()

    def __str__(self):
        return self.title

    def clean(self):
        self.title = self.title.lower()

    def get_absolute_url(self):
        return reverse('tag_filter', args={'tag_title': self.slug})

    class Meta:
        ordering = ['title']
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        verbose_name='Пост, к которому написан'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    text = models.TextField('Текст комментария')
    published_at = models.DateTimeField('Дата и время публикации')

    def __str__(self):
        return f'{self.author.username} under {self.post.title}'

    class Meta:
        ordering = ['published_at']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'