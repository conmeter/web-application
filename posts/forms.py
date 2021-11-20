from django import forms
from .models import Posts


class onWebPostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['review_text', 'design_rating', 'ui_rating', 'speed_rating',
                  'qoc_rating', 'reliability_rating', 'compatibility_rating', 'support_rating', 'trust_rating', 'image']
