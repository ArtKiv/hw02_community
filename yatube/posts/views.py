from django.shortcuts import get_object_or_404, render

from .models import Group, Post

POSTS_PER_PAGE = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()[:POSTS_PER_PAGE]
    context = {
        'posts': posts
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:POSTS_PER_PAGE]
    # posts = Post.objects.filter(group=group)[:COUNT]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
