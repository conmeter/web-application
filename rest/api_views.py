from django.db.models import Avg, Sum
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Posts, Notifications
from rest.serializers import PostSerializer, WebsSerializer, NotificationsSerializer, IssueSerializer
from users.models import User
from webs.models import Webs
from users.serializers import UserSerializer
from users.models import OTPManager


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Posts.objects.filter(user_email=self.request.user).order_by('-date_posted')

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_email=user)


class ProfilePostsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer

    def get_queryset(self):
        return Posts.objects.filter(user_email=self.request.query_params.get('user')).order_by('-date_posted')


class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.query_params.get('user'))


class IssueCreateAPI(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user_email=user)


class PostWeb(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'posts': Posts.objects.filter(web_url=self.request.query_params.get('web_url')). \
                        values('post_id', 'date_posted', 'user_email', 'user_email__name', 'user_email__id', 'web_url',
                               'review_text',
                               'design_rating', 'ui_rating', 'speed_rating', 'qoc_rating', 'reliability_rating',
                               'compatibility_rating', 'support_rating', 'trust_rating', 'total_rating_value',
                               'rating_count',
                               'image').order_by('-date_posted'),
                         'rating': Posts.objects.filter(web_url=self.request.query_params.get('web_url')).aggregate(
                             average_t_r=Avg('total_rating_value'),
                             average_r=Avg('reliability_rating'),
                             average_ui=Avg('ui_rating'),
                             average_spe=Avg('speed_rating'),
                             average_q=Avg('qoc_rating'),
                             average_c=Avg('compatibility_rating'),
                             average_d=Avg('design_rating'),
                             average_su=Avg('support_rating'),
                             average_tr=Avg('trust_rating')),
                         'web': Webs.objects.filter(url=self.request.query_params.get('web_url')).values('url', 'desc',
                                                                                                         'name')
                         })


class WebsViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = WebsSerializer
    queryset = Webs.objects.all()


class WebsAddAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WebsSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserLikesCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if self.request.query_params.get('user'):
            count = Posts.objects.filter(user_email=self.request.query_params.get('user')).aggregate(
                sum_h=Sum('rating_count'))
            return Response(count)
        else:
            count = Posts.objects.filter(user_email=self.request.user).aggregate(sum_h=Sum('rating_count'))
            return Response(count)


class UserPostsCount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if self.request.query_params.get('user'):
            return Response({'count': Posts.objects.filter(user_email=self.request.query_params.get('user')).count()})
        else:
            return Response({'count': Posts.objects.filter(user_email=self.request.user).count()})


import requests
from django.conf import settings


class OTPSystem(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.filter(email=self.request.user).first()
        url = "http://2factor.in/API/V1/" + settings.OTP_API_KEY + "/SMS/" + user.phone + "/AUTOGEN/main"
        response = requests.request("GET", url)
        data = response.json()
        otp = OTPManager.objects.update_or_create(user=self.request.user, defaults={"key": data['Details']})
        return Response({'status': 'OTP SENT'})

    def post(self, request):
        user = User.objects.filter(email=self.request.user).first()
        otp = request.data['otp']
        session = OTPManager.objects.filter(user=self.request.user).values('key')[0]
        url = "http://2factor.in/API/V1/" + settings.OTP_API_KEY + "/SMS/VERIFY/" + session['key'] + "/" + otp + ""
        response = requests.request("GET", url)
        data = response.json()
        if data['Status'] == "Success":
            user.is_verified = True
            user.save()
            return Response({'status': 'success'})
        else:
            return Response({'status': 'failed'})


class SetInActive(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.filter(email=self.request.user).first()
        user.is_verified = False
        user.save()
        return Response({'status': 'success'})


class Tops(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from django.utils import timezone
        import datetime
        last_week = timezone.now() - datetime.timedelta(days=7)
        td = Posts.objects.filter(date_posted__date=timezone.now())
        tw = Posts.objects.filter(date_posted__lte=timezone.now(), date_posted__gt=last_week)
        ta = Posts.objects.all()
        context = {}
        if td:
            td = td.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_day'] = td
        if tw:
            tw = tw.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_week'] = tw
        if ta:
            ta = ta.values('web_url').annotate(a=Avg('total_rating_value')).order_by('-a')[0]
            context['top_all_time'] = ta
        return Response(context)


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = NotificationsSerializer

    def get_queryset(self):
        return Notifications.objects.all().order_by('-date')[:3]
