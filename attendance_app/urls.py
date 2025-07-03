from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('services/', views.services_view, name='services'),
    path("dashboard/", views.employee_login,name='dashboard'),
    path('add-student/', views.add_student, name='add_student'),
    path('mark-attendance/', views.mark_attendance, name='mark_attendance'),
    path('attendance-report/', views.attendance_report, name='attendance_report'),
    path('logout/', views.logout_view, name='logout'),
    path('remove-student/<int:student_id>/', views.remove_student, name='remove_student'),
    path('student_login/', views.student_login, name='student_login'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('daywise/',views.daywise,name='daywise'),
    path('student_daywise/',views.student_daywise,name='student_daywise'),
    path('student_dash/',views.student_dash,name='student_dash'),
    path('forgot/', views.student_forgot_password, name='student_forgot_password'),
    path('admin_login/', views.admin_login, name='admin_login'),



]
