from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import admin
from .models import Webs
from django.contrib.auth.models import Group

admin.site.unregister(Group)

@admin.register(Webs)
class WebsImportExport(ImportExportModelAdmin):
    list_display = ('name', 'url')