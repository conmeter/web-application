from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
import json
from django.shortcuts import render
import re

from django.shortcuts import render, redirect
from .models import Webs
from django.views.generic import CreateView, ListView
from django.db.models import Q
from .forms import WebsRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from posts.models import Posts


class SearchWebsListView(ListView):
    model = Webs
    template_name = 'webs/search-web.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'webs'
    paginate_by = 5

    def get_queryset(self):
        request = self.request
        query = request.GET.get('s_search', None)
        if query is not None:
            return Webs.objects.filter(Q(name__icontains=query)
                                       | Q(url__icontains=query)
                                       | Q(desc__icontains=query)
                                       )
        return Webs.objects.none()


@login_required
def add_web(request):
    if request.method == 'POST':
        form = WebsRegisterForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            name = form.cleaned_data['name']
            desc = form.cleaned_data['desc']
            x = re.sub("www.", "", url)
            y = re.sub("https://", "", x)
            z = re.sub("http://", "", y)
            web_url = Webs()
            web_url.url = z
            web_url.name = name
            web_url.desc = desc
            web_url.save()
            messages.success(request, f'Website added')
            return redirect('web-posts', form['name'].value())
    else:
        form = WebsRegisterForm()
    return render(request, 'webs/add_web.html', {'form': form})


@login_required
def posts_like(request, id):
    get_post = get_object_or_404(Posts, post_id=id)
    rating_status = {}
    if request.is_ajax:
        if request.user in get_post.user.all():
            get_post.rating_count -= 1
            get_post.user.remove(request.user)
            get_post.save()
            rating_status['Removed'] = "True"
            rating_status['count'] = get_post.rating_count
            return HttpResponse(JsonResponse(rating_status))
        else:
            get_post.rating_count += 1
            get_post.user.add(request.user)
            get_post.save()
            rating_status['Success'] = "True"
            rating_status['count'] = get_post.rating_count
            return HttpResponse(JsonResponse(rating_status))
    else:
        rating_status['Success'] = "False"
        return HttpResponse(JsonResponse(rating_status))
    return request
