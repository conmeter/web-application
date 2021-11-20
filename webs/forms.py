import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Webs


class WebsRegisterForm(forms.ModelForm):
    class Meta:
        model = Webs
        fields = ['url', 'name', 'desc']

    def clean(self):
        url = self.cleaned_data['url']
        name = self.cleaned_data['name']
        x = re.sub("www.", "", url)
        y = re.sub("https://", "", x)
        z = re.sub("http://", "", y)

        if Webs.objects.filter(url=z.lower()).exists():
            raise forms.ValidationError("URL already exists")

        if Webs.objects.filter(name=name.lower()).exists():
            raise forms.ValidationError("Name already exists")

