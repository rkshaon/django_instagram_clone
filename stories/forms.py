from django import forms
from django.forms import ClearableFileInput

from stories.models import Story

class NewStoryForm(forms.ModelForm):
    """docstring for NewStoryForm."""
    content = models.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    caption = models.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Story
        fields = ('content', 'caption')
