from import_export import resources

from webs.models import Webs


class WebResource(resources.ModelResource):
    class Meta:
        model = Webs
