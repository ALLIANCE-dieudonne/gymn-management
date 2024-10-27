from django.contrib import admin
from authapp.models import Contact, MembershipPlan, Trainer, Enroll

# Register your models here.
admin.site.register(Contact)
admin.site.register(MembershipPlan)
admin.site.register(Trainer)
admin.site.register(Enroll)