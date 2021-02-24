from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse

from post.models import Post, Stream, Tag
from post.forms import NewPostForm

@login_required
def index(request):
    user = request.user
    posts = Stream.objects.filter(user=user)
    group_ids = []

    for post in posts:
        group_ids.append(post.post_id)

    post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

    context = {
        'post_items': post_items,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

@login_required
def new_post(request):
    user = request.user.id
    tags_obj = []

    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)

        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')

            tags_list = list(tags_form.split(','))

            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_obj.append(t)

            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user)
            p.tags.set(tags_obj)
            p.save()
            return redirect('index')
    else:
        form = NewPostForm()

    context = {
        'form': form,
    }
    template = loader.get_template('new_post.html')
    return HttpResponse(template.render(context, request))

@login_required
def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    context = {
        'post': post,
    }
    template = loader.get_template('post_details.html')
    return HttpResponse(template.render(context, request))

@login_required
def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags=tag).order_by('-posted')

    context = {
        'posts': posts,
        'tag': tag,
    }
    template = loader.get_template('tag.html')
    return HttpResponse(template.render(context, request))