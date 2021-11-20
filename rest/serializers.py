from rest_framework import serializers
from posts.models import Posts, Notifications
from users.models import Issue
from webs.models import Webs


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('post_id', 'web_url', 'review_text',
                  'date_posted', 'design_rating', 'ui_rating',
                  'speed_rating', 'qoc_rating', 'reliability_rating',
                  'compatibility_rating', 'support_rating', 'trust_rating',
                  'total_rating_value', 'rating_count')


class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = ('head', 'body', 'date')


class WebsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webs
        fields = ('url', 'name', 'desc')


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = ('post_id', 'issue_head', 'issue_body')

