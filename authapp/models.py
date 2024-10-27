from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    description = models.TextField()

    def __str__(self):
        return self.email


class Enroll(models.Model):
    fullname = models.CharField(max_length=30)
    email = models.EmailField()
    phoneNumber = models.CharField(max_length=12)
    gender = models.CharField(max_length=25)
    Dob = models.DateField(auto_now=False, auto_now_add=False)
    membershipPlan = models.CharField(max_length=300)
    trainers = models.CharField(max_length=55)
    reference = models.CharField(max_length=55)
    address = models.TextField()
    paymentStatus = models.CharField(max_length=55, blank=True, null=True)
    price = models.IntegerField(max_length=55, blank=True, null=True)
    dueDate = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.fullname


class Trainer(models.Model):
    name = models.CharField(max_length=55)
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=12)
    salary = models.IntegerField(max_length=25)

    def __str__(self):
        return self.name


class MembershipPlan(models.Model):
    plan = models.CharField(max_length=55)
    price = models.IntegerField(max_length=55)

    def __int__(self):
        return self.id
