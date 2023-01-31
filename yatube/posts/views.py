import datetime
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm

from .models import Group, Post, User

POSTS_PER_PAGE = 10


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # posts = Post.objects.filter(group=group)[:COUNT]
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, POSTS_PER_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page_obj.paginator.count
    context = {
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    count = Post.objects.filter(author=post.author).count()
    context = {
        'post': post,
        'count': count,
    }
    return render(request, template, context)


# @login_required
def post_create(request):
    template = 'posts/post_create.html'
    template_redirect = f'/profile/{request.user}/'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(
                author=request.user,
                text=form.cleaned_data['text'],
                group=form.cleaned_data['group'])
            return redirect(template_redirect)
    form = PostForm()
    return render(request, template, {'form': form})


def post_edit(request, post_id):
    template = 'posts/post_create.html'
    template_redirect = f'/profile/{request.user}/'
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():

            post.text = form.cleaned_data['text']
            post.group = form.cleaned_data['group']
            post.pub_date = datetime.datetime.now()
            post.save()
        return redirect(template_redirect)
    form = PostForm(instance=post)
    is_edit = True
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)
