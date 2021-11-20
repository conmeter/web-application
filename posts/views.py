from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Sum
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.template import RequestContext
from django.views.generic import CreateView, ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from posts.models import Posts, Notifications
from webs.models import Webs
from users.models import User, Issue
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from users.forms import IssueForm
from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import onWebPostForm
from django.contrib.auth.decorators import user_passes_test
from page.decorator import active_only


@method_decorator(active_only, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Posts
    template_name = 'posts/feed.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 10

    def get_queryset(self):
        email = get_object_or_404(User, email=self.request.user.email)
        return Posts.objects.filter(user_email=email).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = get_object_or_404(User, email=self.request.user.email)
        context['posts'] = Posts.objects.filter(user_email=email).order_by('-date_posted')
        n = Notifications.objects.all()
        if n:
            context['notif'] = n.order_by('-date')[:3]
        context['tot'] = Posts.objects.filter(user_email=email).aggregate(sum_h=Sum('rating_count'))
        from django.utils import timezone
        import datetime
        last_week = timezone.now() - datetime.timedelta(days=7)
        td = Posts.objects.filter(date_posted__date=timezone.now())
        tw = Posts.objects.filter(date_posted__lte=timezone.now(), date_posted__gt=last_week)
        ta = Posts.objects.all()
        if td:
            td = td.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0] 
            context['top_day'] = get_object_or_404(Webs, url=td['web_url'])
        if tw:
            tw = tw.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_week'] = get_object_or_404(Webs, url=tw['web_url'])
        if ta:
            ta = ta.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_all_time'] = get_object_or_404(Webs, url=ta['web_url'])
        return context


class WebPostListView(ListView):
    model = Posts
    template_name = 'webs/webs.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        web = get_object_or_404(Webs, name=self.kwargs.get('name'))
        return Posts.objects.filter(web_url=web).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        web = get_object_or_404(Webs, name=self.kwargs.get('name'))
        context['w_url'] = Webs.objects.filter(name=web)
        context['tot'] = Posts.objects.filter(web_url=web.url).aggregate(average_t_r=Avg('total_rating_value'),
                                                                         average_r=Avg(
                                                                             'reliability_rating'),
                                                                         average_ui=Avg(
                                                                             'ui_rating'),
                                                                         average_spe=Avg(
                                                                             'speed_rating'),
                                                                         average_q=Avg(
                                                                             'qoc_rating'),
                                                                         average_c=Avg(
                                                                             'compatibility_rating'),
                                                                         average_d=Avg(
                                                                             'design_rating'),
                                                                         average_su=Avg(
                                                                             'support_rating'),
                                                                         average_tr=Avg('trust_rating'))
        from django.utils import timezone
        import datetime
        last_week = timezone.now() - datetime.timedelta(days=7)
        td = Posts.objects.filter(date_posted__date=timezone.now())
        tw = Posts.objects.filter(date_posted__lte=timezone.now(), date_posted__gt=last_week)
        ta = Posts.objects.all()
        if td:
            td = td.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0] 
            context['top_day'] = get_object_or_404(Webs, url=td['web_url'])
        if tw:
            tw = tw.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_week'] = get_object_or_404(Webs, url=tw['web_url'])
        if ta:
            ta = ta.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_all_time'] = get_object_or_404(Webs, url=ta['web_url'])
        return context


class UserPostListView(ListView):
    model = Posts
    template_name = 'posts/users.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, name=self.kwargs.get('name'))
        return Posts.objects.filter(user_email=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = get_object_or_404(User, name=self.kwargs.get('name'))
        context['posts'] = Posts.objects.filter(user_email=email).order_by('-date_posted')
        context['tot'] = Posts.objects.filter(user_email=email).aggregate(sum_h=Sum('rating_count'))
        return context


@method_decorator(active_only, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/feed'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user_email:
            return True
        return False


@active_only
@login_required
def delete_post(request, id):
    if request.is_ajax:
        post = get_object_or_404(Posts, post_id=id)
        post.delete()
        response_data = {'msg': 'Post was deleted.', 'success': 'True'}
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )


@active_only
@login_required
def report_post(request, id):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        post = get_object_or_404(Posts, post_id=id)
        if form.is_valid():
            i = Issue()
            i.post_id = post
            i.user_email = request.user
            i.issue_head = form.cleaned_data['issue_head']
            i.issue_body = form.cleaned_data['issue_body']
            i.save()
            messages.success(request, f'Issue has been reported!')
            return redirect('feed')

    else:
        form = IssueForm()
    return render(request, 'users/issue_form.html', {'form': form})


@method_decorator(active_only, name='dispatch')
@method_decorator(login_required, name='dispatch')
class PostCreateResponseView(CreateView):
    model = Posts
    fields = ['web_url', 'review_text', 'design_rating', 'ui_rating', 'speed_rating',
              'qoc_rating', 'reliability_rating', 'compatibility_rating', 'support_rating', 'trust_rating', 'image']
    success_url = '/feed'

    def form_valid(self, form):
        form.instance.user_email = self.request.user
        return super().form_valid(form)


@active_only
@login_required
def createOnPost(request, pk):
    if request.method == 'POST':
        form = onWebPostForm(request.POST, request.FILES)
        k = get_object_or_404(Webs, url=pk)
        if form.is_valid():
            i = Posts()
            i.web_url = k
            i.user_email = request.user
            i.review_text = form.cleaned_data['review_text']
            i.design_rating = form.cleaned_data['design_rating']
            i.ui_rating = form.cleaned_data['ui_rating']
            i.speed_rating = form.cleaned_data['speed_rating']
            i.qoc_rating = form.cleaned_data['qoc_rating']
            i.reliability_rating = form.cleaned_data['reliability_rating']
            i.compatibility_rating = form.cleaned_data['compatibility_rating']
            i.support_rating = form.cleaned_data['support_rating']
            i.trust_rating = form.cleaned_data['trust_rating']
            i.image = form.cleaned_data['image']
            i.save()
            messages.success(request, f'Post Generated')
            return redirect('web-posts', name = k.name)
    else:
        form = onWebPostForm()
    return render(request, 'posts/post_form_direct.html', {'form': form})

