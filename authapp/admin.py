from django.contrib import admin
from authapp.models import Contact, MembershipPlan, Trainer, Enroll, Gallery, Attendance

# Register your models here.
admin.site.register(Contact)
admin.site.register(MembershipPlan)
admin.site.register(Trainer)
admin.site.register(Enroll)
admin.site.register(Gallery)
admin.site.register(Attendance)