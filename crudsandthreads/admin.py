from django.contrib import admin
from crudsandthreads import models as ctmodels


class StudentAdmin(admin.ModelAdmin):
    pass


admin.site.register(ctmodels.Student, StudentAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    pass


admin.site.register(ctmodels.Attendance, AttendanceAdmin)
