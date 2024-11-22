from django.urls import path
from authapp import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("contact", views.contact_view, name="contact"),
    path('enroll', views.enroll, name="enroll"),
    path('profile', views.profile, name="profile"),
    path('gallery', views.gallery, name="gallery"), 
    path('attendance', views.attendance, name="attendance"),
    path('dashboard', views.dashboard, name="dashboard")
]
