from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.https import JsonResponse
from datetime import datetime, timedelta

from stories.models import Story, StoryStream
from stories.forms import NewStoryForm

@login_required
def new_story(request):
    user = request.user
    file_objs = []

    if request.method == 'POST':
        form = NewStoryForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('content')
            caption = form.cleaned_data.get('caption')

            story = Story(user=user, content=file, caption=caption)
            story.save()

            return redirect('index')
    else:
        form = NewStoryForm()

    context = {
        'form': form,
    }

    return render(request, 'new_story.html', context)
