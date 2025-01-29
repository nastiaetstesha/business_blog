from django.shortcuts import render, get_object_or_404
from blog.models import Comment, Post, Tag
from django.db.models import Count


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.comments_count,  # ✅ Используем `annotate()`
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.first().title if post.tags.exists() else None,  # ✅ Проверяем на пустоту
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': getattr(tag, 'posts_count', 0),  # ✅ Проверяем, есть ли аннотация `posts_count`
    }


def index(request):
    most_popular_posts = (
        Post.objects
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),  # ✅ `related_name="comments"`?
        )
        .only('id', 'title', 'text', 'slug', 'image', 'published_at', 'author_id')  # ✅ Добавили `author_id`
        .select_related('author')
        .prefetch_related('tags', 'likes')
        .order_by('-likes_count')[:5]
    )

    most_popular_tags = (
        Tag.objects
        .annotate(posts_count=Count('posts'))  # ✅ Аннотируем `posts_count`
        .order_by('-posts_count')[:5]
    )

    fresh_posts = (
        Post.objects
        .annotate(comments_count=Count('comments', distinct=True))
        .only('id', 'title', 'text', 'slug', 'image', 'published_at', 'author_id')
        .select_related('author')
        .prefetch_related('tags')
        .order_by('-published_at')[:5]
    )

    context = {
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts],
        'page_posts': [serialize_post(post) for post in fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )
        .select_related('author')
        .prefetch_related('tags', 'likes', 'comments__author')  # ✅ Загружаем комменты за 1 SQL-запрос
        .only('id', 'title', 'text', 'slug', 'image', 'published_at', 'author_id')
        .filter(slug=slug)
    )

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': [
            {'text': comment.text, 'published_at': comment.published_at, 'author': comment.author.username}
            for comment in post.comments.all()
        ],
        'likes_amount': post.likes_count,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
    }

    most_popular_tags = (
        Tag.objects
        .annotate(posts_count=Count('posts'))
        .order_by('-posts_count')[:5]
    )

    most_popular_posts = (
        Post.objects
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )
        .select_related('author')
        .prefetch_related('tags', 'likes')
        .order_by('-likes_count')[:5]
    )

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    tag = get_object_or_404(
        Tag.objects
        .annotate(posts_count=Count('posts'))  # ✅ Добавили аннотацию `posts_count`
        .filter(title=tag_title)
    )

    most_popular_tags = (
        Tag.objects
        .annotate(posts_count=Count('posts'))
        .order_by('-posts_count')[:5]
    )

    most_popular_posts = (
        Post.objects
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )
        .select_related('author')
        .prefetch_related('tags', 'likes')
        .order_by('-likes_count')[:5]
    )

    related_posts = (
        tag.posts
        .annotate(
            likes_count=Count('likes', distinct=True),
            comments_count=Count('comments', distinct=True),
        )
        .select_related('author')
        .prefetch_related('tags', 'likes')
        .order_by('-published_at')[:20]
    )

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [serialize_post(post) for post in most_popular_posts],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    return render(request, 'contacts.html', {})
