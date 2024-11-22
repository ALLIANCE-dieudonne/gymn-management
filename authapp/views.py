from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from authapp.models import Contact, MembershipPlan, Trainer, Enroll, Gallery, Attendance
from django.db.models import Count
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta, date
import json


def Home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get("usernumber")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirmation = request.POST.get("password_confirmation")

        # Check username length
        if len(username) != 10:
            messages.warning(request, "Phone number must be 10 characters")
            return redirect("/signup")

        # Check if passwords match
        if password != password_confirmation:
            messages.warning(request, "Passwords do not match")
            return redirect("/signup")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username already exists")
            return redirect("/signup")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists")
            return redirect("/signup")

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
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect("/login")

    user_phone = request.user
    posts = Enroll.objects.filter(phoneNumber=user_phone)
    context = {"posts": posts}
    return render(request, "profile.html", context)


def gallery(request):
    images = Gallery.objects.all()
    context = {"images": images}
    return render(request, "gallery.html", context)


def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login first.")
        return redirect("/login")

    trainers = Trainer.objects.all()
    context = {"trainers": trainers}

    if request.method == "POST":
        phoneNumber = request.POST.get("number")
        selectDate = request.POST.get("selectDate")
        login_time = request.POST.get("login")
        logout_time = request.POST.get("logout")
        selectWorkout = request.POST.get("workout")
        trainedBy = request.POST.get("trainer")

        attendance_records = Attendance.objects.filter(phoneNumber=phoneNumber)

        if attendance_records.exists():
            attendance_record = attendance_records.first()
            attendance_record.login = login_time
            attendance_record.logout = logout_time
            attendance_record.selectWorkout = selectWorkout
            attendance_record.trainedBy = trainedBy
            attendance_record.save()
            messages.info(request, "Attendance record updated successfully.")
        else:
            query = Attendance(
                phoneNumber=phoneNumber,
                selectDate=selectDate,
                login=login_time,
                logout=logout_time,
                trainedBy=trainedBy,
                selectWorkout=selectWorkout,
            )
            query.save()
            messages.info(request, "Attendance record created successfully.")

        return redirect("/attendance")

    return render(request, "attendance.html", context)


def dashboard(request):
    try:
        # Hardcoded Statistics
        stats = {
            "total_members": Enroll.objects.count(),
            "total_trainers": Trainer.objects.count(),
            "total_plans": MembershipPlan.objects.count(),
            "today_attendance": Attendance.objects.filter(
                selectDate=datetime.now().date()
            ).count(),
        }

      

        membership_distribution = (
            MembershipPlan.objects.values("plan")
            .annotate(count=Count("id"))
            .order_by("plan")
        )
        membership_distribution = [
            {"membershipPlan": item["plan"], "count": item["count"]}
            for item in membership_distribution
        ]

       
        monthly_enrollments =(
            Enroll.objects
            .annotate(month=TruncMonth('timestamp'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        
        formatted_monthly_enrollments = [
            {"month": item["month"].strftime("%Y-%m-%d"), "count": item["count"]}
            for item in monthly_enrollments
        ]
        

        
        today = date.today()
        one_week_ago = today - timedelta(days=6)

        weekly_attendance = (
            Attendance.objects.filter(selectDate__range=[one_week_ago,today])
            .values('selectDate').annotate(count=Count('id')).order_by('selectDate')
        )

        formatted_weekly_attendance = [
            {"date": item["selectDate"].strftime("%Y-%m-%d"), "count": item["count"]}
            for item in weekly_attendance
        ]
        
       

        recent_enrollments_queryset = Enroll.objects.order_by('-timestamp')[:5]
        recent_enrollments = [
            {"fullname": enroll.fullname,
            "membershipPlan": enroll.membershipPlan,
            "phoneNumber": enroll.phoneNumber,
            "timestamp": enroll.timestamp.strftime('%Y-%m-%d'),
            }
            for enroll in recent_enrollments_queryset
        ]

        context = {
            "stats": stats,
            "membership_distribution": json.dumps(membership_distribution),
            "monthly_enrollments": json.dumps(formatted_monthly_enrollments),
            "attendance_trend": json.dumps(formatted_weekly_attendance),
            "recent_enrollments": recent_enrollments,
        }

        return render(request, "dashboard.html", context)

    except Exception as e:
        print(f"Dashboard Error: {str(e)}")
        return render(request, "dashboard.html", {"error": str(e)})
