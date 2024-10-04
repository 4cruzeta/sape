from django import forms
from django.utils.translation import gettext_lazy as _
from . import models 

class CreatePost(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body']
        labels = {
            'title': _('Title'),
            'body': _('Body'),
        }