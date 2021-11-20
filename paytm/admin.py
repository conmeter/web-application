from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from paytm.models import PaytmHistory


class Transaction(admin.ModelAdmin):
    list_display = ('order_id', 'made_by', 'made_on', 'amount', 'status',)
    search_fields = ['order_id', 'made_by__email', 'made_on', 'amount', 'status',]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(PaytmHistory)
class ViewAdmin(ImportExportModelAdmin, Transaction):

    def has_import_permission(self, request):
        return False
