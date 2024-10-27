from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authapp.models import Contact, MembershipPlan, Trainer, Enroll


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


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        message = request.POST.get("desc")
        myQuery = Contact(
            name=name, email=email, phoneNumber=number, description=message
        )
        myQuery.save()
        messages.info(request, "Thanks for contacting us.We will reach you soon!")
        return redirect("/contact")
    return render(request, "contact.html")


def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You need to be logged in to enroll.")
        return redirect("/login")
    
    Membership = MembershipPlan.objects.all()
    trainers = Trainer.objects.all()
    context = {"Membership": Membership, "trainers": trainers}

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phoneNumber = request.POST.get("number")
        gender = request.POST.get("gender")
        Dob = request.POST.get("dob")
        membership = request.POST.get("membershipPlan")
        address = request.POST.get("address")
        trainers = request.POST.get("trainer")
        reference = request.POST.get("reference")
        query = Enroll(
            fullname=fullname,
            email=email,
            phoneNumber=phoneNumber,
            gender=gender,
            Dob=Dob,
            membershipPlan=membership,
            trainers=trainers,
            reference=reference,
            address=address,
        )
        query.save()
        messages.info(request, "You have successfully enrolled.")
        return redirect("/enroll")
    return render(request, "enroll.html", context)

def profile(request):
    return render(request, "profile.html")
