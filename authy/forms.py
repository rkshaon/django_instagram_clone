from django import forms
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from authy.models import Profile

def ForbiddenUsers(value):
    forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
    if value.lower() in forbidden_users:
        raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('User with this email already exists.')

def UniqueUser(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('User with this username already exists.')

class SignupForm(forms.ModelForm):
    """ describing sign up form """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), max_length=30, required=True,)
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'input is-medium'}), max_length=100, required=True,)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input is-medium'}), required=True, label="Confirm your password.")
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(ForbiddenUsers)
        self.fields['username'].validators.append(InvalidUser)
        self.fields['username'].validators.append(UniqueUser)
        self.fields['email'].validators.append(UniqueEmail)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
        return self.cleaned_data

class EditProfileForm(forms.ModelForm):
    """docstring for EditProfileForm."""
    picture = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    location = forms.CharField(widget=forms.TextInput(), max_length=25, required=False)
    url = forms.URLField(widget=forms.TextInput(), max_length=60, required=False)
    profile_info = forms.CharField(widget=forms.TextInput(), max_length=260, required=False)

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name', 'location', 'url', 'profile_info')
