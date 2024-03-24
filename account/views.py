from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import KYC, Account
from account.forms import KYCForm
from core.forms import CreditCardForm
from core.models import CreditCard

# @login_required
def account(request):
    # You can use this instead of Login_required
    if request.user.is_authenticated:
        try:
            # Try to get KYC information for the user
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submir your KYC")
            return redirect("account:kyc-reg")
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the Dashboard")
        return redirect("userauths:sign_in")

    context = {
        "kyc" :kyc,
        "account": account
    }

    return render(request, "account/account.html", context)


@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=request.user)

    try:
        kyc = KYC.objects.get(user=user)
    except KYC.DoesNotExist:
        kyc = None

    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)

        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            # return redirect("account:transaction-pin")
            # messages.success(request, "KYC form submitted successfully. In review now.")
            return redirect("account:dashboard")

        else:
            # Print form errors to the console for debugging
            print(form.errors)
            messages.error(request, "Error submitting KYC form. Please check the form for errors.")
    else:
        form = KYCForm(instance=kyc)

    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "account/kyc-form.html", context)

@login_required
def dashboard(request):
    if request.user.is_authenticated:
        try:
            # Try to get KYC information for the user
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submir your KYC")
            return redirect("account:kyc-reg")
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by("-id")

        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()

                card_id = new_form.card_id
                messages.success(request, "Card added successfully")
                return redirect("account:dashboard")
        else:
            form = CreditCardForm()


    else:
        messages.warning(request, "You need to login to access the Dashboard")
        return redirect("userauths:sign-in")

    context = {
        "kyc" :kyc,
        "account": account,
        "form":form,
        "credit_card": credit_card
    }


    return render(request, "account/dashboard.html", context)

# def transaction_pin(request):

#     return render(request, "transaction/transaction-pin.html")
