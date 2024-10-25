from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def Home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("usernumber")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        # Check username length
        if len(username) != 5:
            messages.warning(request, "Phone number must be 10 characters")
            return redirect("/signup")

        # Check if passwords match
        if password != password_confirmation:
            messages.warning(request, "Passwords do not match")
            return redirect("/signup")

        # Check if username already exists
        try:
            if User.objects.get(username=username):
                messages.warning(request, "Username already exists")
                return redirect("/signup")
        except User.DoesNotExist:
            pass

        # Check if email already exists
        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email already exists")
                return redirect("/signup")
        except User.DoesNotExist:
            pass

        # Create the user
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.save()
        messages.success(request, "User created successfully")
        return redirect("/login")

    return render(request, "signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("usernumber")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("/")
        else:
            messages.warning(request, "Invalid credentials")
            return redirect("/login")
    return render(request, "login.html")

def logout_view(request):
    logout(request)  # Ends session and logs out user
    messages.success(request, "Logged out successfully")
    return redirect("/login")  # Redirect to login page
