from import_export import resources
from posts.models import Posts
from users.models import Issue, User

class PostsResource(resources.ModelResource):
    class Meta:
        model = Posts


class IssuesResource(resources.ModelResource):
    class Meta:
        model = Issue

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        exclude = ('is_moderator','is_staff', 'is_superuser',
         'is_active', 't_c', 'password', 'groups', 'user_permissions', 'id')

    def export(self, queryset=None, *args, **kwargs):
        queryset = User.objects.filter(email=kwargs['agent'])
        return super(UserResource, self).export(queryset, *args, **kwargs)