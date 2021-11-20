from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User, Issue


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['name', 'phone', 'dob', 'email', 'password1', 'password2', 't_c']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['name', 'phone', 'dob', 'email', 'image']


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['issue_head', 'issue_body']


from django.contrib.auth.forms import AuthenticationForm

class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass