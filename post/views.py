from django.shortcuts import render, redirect
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
