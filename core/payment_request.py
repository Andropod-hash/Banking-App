from account.models import Account
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction
from decimal import Decimal
from decimal import Decimal


@login_required
def SearchUsersRequest(request):
    account = Account.objects.alBl()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct

    context = {
        "account": account,
        "query": query,
    }

    return render(request, "payment_requests/search-users.html", context)

def AmountRequest(request, account_number):
    account = Account.objects.get(account_number=account_number)

    context = {
        "account": account
    }

    return render(request, "payment_requests/amount-request.html", context)


def AmountRequestProcess(request, account_number):
    # Fetch the account based on the provided account_number
    account = Account.objects.get(account_number=account_number)

    # Extract the sender and receiver information
    sender = request.user
    reciever = account.user

    # Extract the sender and receiver account objects
    sender_account = request.user.account
    reciever_account = account

    # Check if the request method is POST
    if request.method == "POST":
        # Extract amount and description from the POST data
        amount = request.POST.get("amount-request")
        description = request.POST.get("description")

        # Create a new Transaction object and save it to the database
        new_request = Transaction.objects.create(
            user=sender,
            amount=amount,
            description=description,
            reciever_account=reciever_account,
            sender_account=sender_account,
            status="request_processing",
            transaction_type="request"
        )

        # Save the new transaction
        new_request.save()

        # Get the transaction_id for redirecting to the confirmation page
        transaction_id = new_request.transaction_id

        # Redirect to the confirmation page with the necessary parameters
        return redirect("core:amount-request-confirmation", account.account_number, transaction_id)

    else:
        # If the request method is not POST, show a warning message and redirect to the dashboard
        print(form.errors)
        messages.warning(request, "Error occurred here, try again later.")
        return redirect("account:dashboard")

def AmountRequestConfirmation(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        "account":account,
        "transaction": transaction
    }

    return render(request, "payment_requests/amount-request-confirmation.html", context)

def AmountRequestFinalProcess(request, account_number, transaction_id):
    # Fetch the account based on the provided account_number
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")

        # Check if the pin_number matches the user's account pin_number
        if pin_number == request.user.account.pin_number:
            transaction.status = "request_sent"
            transaction.save()

            messages.success(request, "Your payment request has been completed")
            return redirect("core:amount-request-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "An Error Occurred, try again")
            return redirect("account:dashboard")

def RequestCompleted(request, account_number, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    account = Account.objects.get(account_number=account_number)

    context = {
        "account":account,
        "transaction": transaction
    }

    return render(request, "payment_requests/amount-request-completed.html", context)



