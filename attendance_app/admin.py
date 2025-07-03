from django.contrib import admin
from .models import Student, StudentLogin

#admin.site.register(Student)
#admin.site.register(StudentLogin)

from django.contrib import admin
from .models import Student, Attendance, StudentLogin
from django.contrib.auth.models import User

class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'section')
    search_fields = ('name', 'roll_number', 'section')
    list_filter = ('section',)

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'is_present')
    search_fields = ('student__name', 'student__roll_number')
    list_filter = ('date', 'student__section')

class StudentLoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')
    search_fields = ('username',)

admin.site.register(Student, StudentAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(StudentLogin, StudentLoginAdmin)
