from django.contrib import admin

# Register your models here.

from account.models import Account, KYC
from userauths.models import User
# from import_export.admin import ImportExportAdmin
from import_export.admin import ImportExportMixin, ImportExportActionModelAdmin


class AccountAdminModel(ImportExportActionModelAdmin):
    list_editable = ['account_status', 'account_balance']
    list_display = ['user', 'account_number', 'account_status', 'account_balance']
    list_filter = ['account_status']

class KYCAdmin(ImportExportActionModelAdmin):
    search_fields = ["full_name"]
    list_display = ["user", "full_name"]

# class Pin_NumberAdmin(ImportExportActionModelAdmin):
#     list_display = ["user", "pin_number"]

admin.site.register(Account, AccountAdminModel)
admin.site.register(KYC, KYCAdmin)
# admin.site.register(Pin_Number, Pin_NumberAdmin)

