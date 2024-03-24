from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from userauths.models import User
# Create your views here.

def Registerview(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("account:kyc-reg")
            # return redirect("core:index")

    # elif request.user.is_authenticated:
    #     username = request.user.username  # Retrieve the username from the authenticated user
    #     messages.warning(request, f"Hey {username}, You are already logged in")
    #     return redirect("core:index")


    else:
        form = UserRegisterForm()

    context = {
        "form": form
    }
    return render(request, "userauths/sign-up.html", context)

def LoginView(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None: # Check if there is a user
                login(request, user)
                messages.success(request, "You are logged in usuccesfully")
                return redirect("acount:account")
            else:
                messages.warning(request, "Username or Passworf does not exist")
                return redirect("userauths:sign-in")
        except:
            messages.warning(request, "User does not exist")
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect("account:account")


    return render(request, "userauths/sign-in.html")

def LogoutView(request):
        # print(request.user.username)
        logout(request)
        messages.success(request, "You have been logged out")
        return redirect("userauths:sign-in")



