from django import forms
from post.models import Post

class NewPostForm(forms.ModelForm):
    """docstring for NewPostForm."""
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-mediam'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)

    class Meta:
        model = Post
        fields = ('picture', 'caption', 'tags')
