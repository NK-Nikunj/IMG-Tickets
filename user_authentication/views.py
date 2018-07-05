from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, get_user_model, login, logout

from .forms import UserLoginForm, UserRegisterForm

# View for login
def login_view(request):

    # determining the page type
    page_type = "Log In"

    # get form
    form = UserLoginForm(request.POST or None)

    # validate form
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        # authenticate user again, just to be double sure
        user = authenticate(username=username, password=password)
        login(request, user) # login the user
        return redirect("tickets/") # redirect user

    # items to render
    context = {
        "form": form,
        "page_type": page_type,
    }
    return render(request, "accounts/login.html", context)



# View for sign up
def register_view(request):

    # detemining the page type
    page_type = "Sign Up"

    # get form
    form = UserRegisterForm(request.POST or None)

    # validate form
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user.save() # save the user

        # authenitcate the user again, just to be sure
        new_user = authenticate(username=username, password=password)
        login(request, user) # login the user
        return redirect("tickets/") # redirect user

    # items to render
    context = {
        "form": form,
        "page_type": page_type,
    }
    return render(request, "accounts/login.html", context)


# View for Logout
def logout_view(request):
    logout(request) # logout the user
    return redirect("/") # redirect to login page
