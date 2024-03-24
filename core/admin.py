from django.contrib import admin
from core.models import Transaction, CreditCard

# Register your models here.

class TransactionAdmin(admin.ModelAdmin):
    list_editable = ["amount", "status", "transaction_type", "reciever", "sender"]
    list_display = ["user", "amount", "status", "transaction_type", "reciever", "sender"]


class CreditCardAdmin(admin.ModelAdmin):
    list_editable = ["amount", "card_type"]
    list_display = ["user", "amount", "card_type"]  # Assuming you want to display "user", "account", and "card_type"

admin.site.register(Transaction, TransactionAdmin)

admin.site.register(CreditCard, CreditCardAdmin)