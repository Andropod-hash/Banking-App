from django.urls import path
from core import views, transfer, transaction, payment_request, credit_card
from core.payment_request import AmountRequestConfirmation




app_name = 'core'

urlpatterns = [
    path("", views.index, name="index" ),

    # Transfer
    path("search-account", transfer.search_users_account_number, name="search-account" ),
    path("amount-transfer/<account_number>/", transfer.AmountTransfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>", transfer.TransferConfirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>", transfer.TransferProcess, name="transfer-process"),
    path("transfer-completed/<account_number>/<transaction_id>", transfer.TransferCompleted, name="transfer-completed"),

    # Transactions
    path("transaction/", transaction.transaction_lists, name="transactions"),
    path("transaction/<transaction_id>/", transaction.transaction_detail, name="transaction-detail"),

    # Payment Requests
    path("request-search-account/", payment_request.SearchUsersRequest, name="request-search-account"),
    path("amount-request/<account_number>/", payment_request.AmountRequest, name="amount-request"),
    path("amount-request-process/<account_number>/", payment_request.AmountRequestProcess, name="amount-request-process"),
    path("amount-request-confirmation/<account_number>/<transaction_id>", payment_request.AmountRequestConfirmation, name="amount-request-confirmation"),
    path("amount-request-final-process/<account_number>/<transaction_id>", payment_request.AmountRequestFinalProcess, name="amount-request-final-process"),
    path("amount-request-completed/<account_number>/<transaction_id>", payment_request.RequestCompleted, name="amount-request-completed"),

    # Credit card url

    path("card/<card_id>/", credit_card.card_detail, name="card-detail"),
    path("fund-credit-card/<card_id>/", credit_card.fund_credit_card, name="fund-credit-card"),
    path("withdraw_fund/<card_id>/", credit_card.withdraw_fund, name="withdraw_fund"),
    path("delete_card/<card_id>/", credit_card.delete_card, name="delete_card")






]
