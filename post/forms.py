from django import forms
from django.forms import ClearableFileInput

from post.models import Post

class NewPostForm(forms.ModelForm):
    """docstring for NewPostForm."""
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-mediam'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        fields = ('content', 'caption', 'tags')
