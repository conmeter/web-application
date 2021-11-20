

from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect


def active_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_active and request.user.is_verified:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('logout')
    return wrap