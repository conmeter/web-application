from .resources import PostsResource, IssuesResource, UserResource
from .render import Render
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from users.forms import UserRegisterForm, UserUpdateForm, IssueForm
from users.models import Issue, User
from posts.models import Posts
from django.core import serializers
import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from page.decorator import active_only
from django.conf import settings

def register(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user_phone = form.cleaned_data.get('phone')
            request.session['user_phone'] = user_phone
            response = gen_otp(request, user_phone)
            data = response.json()
            request.session['otp_session_data'] = data['Details']
            messages.success(
                request, f'Your account has been created! OTP has been sent to your phone number')
            
            return redirect('otp_ck')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def gen_otp(request, user_phone):
    url = "http://2factor.in/API/V1/"+settings.OTP_API_KEY+"/SMS/" + user_phone + "/AUTOGEN/main"
    response = requests.request("GET", url)
    return response
    
def otp_ck(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        user_phone = request.session['user_phone']
        url = "http://2factor.in/API/V1/"+settings.OTP_API_KEY+"/SMS/VERIFY/" + request.session['otp_session_data'] + "/" + user_otp + ""
        response = requests.request("GET", url)
        data = response.json()
        if data['Status'] == "Success":
            o = get_object_or_404(User, phone= user_phone)
            o.is_verified = True
            o.save()
            messages.success(request, f'Verification successful please log in below.')
            return redirect('login')
        else:
            messages.success(request, f'WRONG OTP')
    return render(request,'page/otp_page.html', {'phno' : request.session['user_phone']})


def otp_ck_2(request):
    if request.method == "POST":
        user_otp = request.POST['otp']
        user_phone = request.session['user_phone']
        url = "http://2factor.in/API/V1/"+settings.OTP_API_KEY+"/SMS/VERIFY/" + request.session['otp_session_data'] + "/" + user_otp + ""
        response = requests.request("GET", url)
        data = response.json()
        if data['Status'] == "Success":
            o = get_object_or_404(User, phone= request.session['old_phone'])
            o.phone = user_phone
            o.is_verified = True
            o.save()
            messages.success(request, f'Verification successful please log in below.')
            return redirect('login')
        else:
            messages.success(request, f'WRONG OTP')
    return render(request,'page/otp_page.html', {'phno' : request.session['user_phone']})

def resend_otp(request):
    user_phone = request.session['user_phone']
    response = gen_otp(request, user_phone)
    data = response.json()
    request.session['otp_session_data'] = data['Details']
    messages.success(request, f'OTP has been sent to your phone number')
    return redirect('otp_ck')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@active_only
@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            o = get_object_or_404(User, email = request.user.email)
            old_phone = o.phone
            if u_form.cleaned_data.get('phone') != o.phone:
                u_form.save()
                o = get_object_or_404(User, email = request.user.email)
                o.is_verified = False
                o.phone = old_phone
                o.save()
                user_phone = u_form.cleaned_data.get('phone') 
                request.session['user_phone'] = user_phone
                request.session['old_phone'] = old_phone
                response = gen_otp(request, user_phone)
                data = response.json()
                request.session['otp_session_data'] = data['Details']
                messages.success(request, f'Your account has been updated! OTP has been sent to your phone number')
                return redirect('otp_ck_2')
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('feed')

    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }

    return render(request, 'users/user_updating.html', context)

def change_number(request):
    if request.method == "POST":
        user_phone = request.POST['num']
        o = get_object_or_404(User, phone=request.session['user_phone'])
        old_phone = request.session['user_phone']
        request.session['user_phone'] = user_phone
        request.session['old_phone'] = old_phone
        try:
            o.phone = user_phone
            o.save()
            o.phone = old_phone
            o.save()
            response = gen_otp(request, user_phone)
            data = response.json()
            request.session['otp_session_data'] = data['Details']
            messages.success(request, f'OTP has been sent to your phone number')
            return redirect('otp_ck_2')
        except:
            messages.success(request, f'Please check your phone number! This number is already taken')
    return render(request, 'page/change_number.html')



@active_only
@login_required
def issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            i = Issue()
            i.user_email = request.user
            i.issue_head = form.cleaned_data['issue_head']
            i.issue_body = form.cleaned_data['issue_body']
            i.save()
            messages.success(request, f'Issue has been reported!')
            return redirect('feed')

    else:
        form = IssueForm()
    return render(request, 'users/issue_form.html', {'form': form})



@active_only
@login_required
def export_posts(request):
    posts_resource = PostsResource()
    dataset = posts_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="posts.csv"'
    return response


@active_only
@login_required
def export_issues(request):
    issue_resource = IssuesResource()
    dataset = issue_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="issue.csv"'
    return response


@active_only
@login_required
def export_user(request):
    user_resource = UserResource()
    dataset = user_resource.export(agent=request.user)
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="user.csv"'
    return response


@active_only
@login_required
def download_user_data(request):
    return render(request, 'users/user_data.html')


from users.forms import AuthenticationFormWithInactiveUsersOkay
from django.contrib.auth import authenticate, login


def login_request(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = AuthenticationFormWithInactiveUsersOkay(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active and user.is_verified:
                    login(request, user)
                    return redirect('feed')
                else:
                    o = get_object_or_404(User, email=user)
                    request.session['user_phone'] = o.phone
                    response = gen_otp(request, request.session['user_phone'])
                    data = response.json()
                    request.session['otp_session_data'] = data['Details']
                    messages.success(request, f'Looks like your account is not active, please activate it below.')
                    return redirect('otp_ck')
                    
            else:
                messages.success(request, "Invalid username or password.")
        else:
            messages.success(request, "Invalid username or password.")
    form = AuthenticationFormWithInactiveUsersOkay()
    return render(request = request, template_name = "users/login.html", context={"form":form})


@active_only
@login_required
def disable_account(request):
    obj = get_object_or_404(User, email=request.user.email)
    obj.is_verified = False
    obj.save()
    messages.success(request, f'ACCOUNT DISABLED! Please login and verify to re-enable account')
    return redirect('logout')

