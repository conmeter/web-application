from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from posts.models import Posts
from django.contrib.auth.decorators import user_passes_test
from page.decorator import active_only



def home(request):
    count = Posts.objects.all().count()
    return render(request, 'page/index.html', {'count': count})


@active_only
@login_required
def feed(request):
    return render(request, 'page/success_login.html')


def handler404(request, exception):
    context = RequestContext(request)
    err_code = 404
    response = render_to_response('page/custom_404.html', {"code": err_code}, context)
    response.status_code = 404
    return response

def handler500(request):
    return render(request, 'page/custom_404.html')

import json
from django.http import HttpResponse, HttpResponseRedirect


def send_count(request):
    if request.is_ajax:
        count = Posts.objects.all().count()
        response_data = {'count': count, 'success': 'True'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
