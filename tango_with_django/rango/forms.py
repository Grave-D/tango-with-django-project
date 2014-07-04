from django.contrib.auth.models import User

__author__ = 'user'

from django import forms
from models import Category, Page, UserProfile


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Enter category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # Inline class to provide additional information on form
    class Meta:
        # Provides association between ModelForm and model
        model = Category

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter page title")
    url = forms.URLField(max_length=200, help_text="Enter URL of the page")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    # Inline class to provide additional information on form
    class Meta:
        # Provides association between ModelForm and model
        model = Page
        # You can choose what fields to show
        # !!!Hidden inputs still need to be in "fields"
        fields = ('title', 'url', 'views')

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # if url is not empty and it doesn't start with "http://",
        # add 'http://' at the start
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="Please enter a username")
    email = forms.CharField(help_text="Please enter an email")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Please enter a password")

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(help_text="Pleasse enter your website", required=False)
    picture = forms.ImageField(help_text="Select a profile image to upload", required=False)

    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
