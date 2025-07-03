from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from .models import Student, Attendance
from django.utils import timezone

def home_view(request):
    return render(request, 'attendance_app/index.html')

def about_view(request):
    return render(request, 'attendance_app/about.html')

def contact_view(request):
    return render(request, 'attendance_app/contact.html')

def services_view(request):
    return render(request, 'attendance_app/services.html')

def register_view(request):
    return render(request, 'attendance_app/register.html')

def login_view(request):
    return render(request, 'attendance_app/login.html')

def employee_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return render(request, 'attendance_app/dashboard.html')  # ✅ Go to dashboard
        else:
            messages.error(request, "Invalid credentials or not a superuser")
            return render(request, 'attendance_app/login.html')  # ✅ Correct fallback

    return render(request, 'attendance_app/login.html')  # ✅ GET fallback

@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'attendance_app/dashboard.html')

'''
@login_required(login_url='/login/')
def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        roll = request.POST['roll_number']
        section = request.POST['section']
        Student.objects.create(name=name, roll_number=roll, section=section)
        return redirect('add_student')

    students = Student.objects.all()
    return render(request, 'attendance_app/add_student.html', {'students': students})
'''

import pandas as pd
from django.contrib import messages

@login_required(login_url='/login/')
def add_student(request):
    if request.method == "POST":
        if 'single_add' in request.POST:
            # Single student
            name = request.POST['name']
            roll_number = request.POST['roll_number']
            section = request.POST['section']

            Student.objects.create(name=name, roll_number=roll_number, section=section)
            messages.success(request, "Student added successfully!")
            return redirect('add_student')

        elif 'bulk_add' in request.POST:
            # Bulk add
            file = request.FILES.get('file')

            if not file:
                messages.error(request, "Please upload a file.")
                return redirect('add_student')

            try:
                # Try reading Excel or CSV
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                # Expecting columns: Name, RollNumber, Section
                for index, row in df.iterrows():
                    name = str(row['Name']).strip()
                    roll_number = str(row['RollNumber']).strip()
                    section = str(row['Section']).strip()

                    if name and roll_number and section:
                        Student.objects.create(name=name, roll_number=roll_number, section=section)

                messages.success(request, "Students added successfully!")
                return redirect('add_student')

            except Exception as e:
                print(e)
                messages.error(request, "Error processing file: " + str(e))
                return redirect('add_student')

    students = Student.objects.all()
    return render(request, 'attendance_app/add_student.html', {'students': students})




from datetime import date
@login_required(login_url='/login/')
def mark_attendance(request):
    students = None
    if request.method == 'POST':
        section = request.POST.get('section')
        students = Student.objects.filter(section=section)

        if 'submit_attendance' in request.POST:
            today = date.today()

            marked_ids = []

            for student in students:
                status = request.POST.get(f'attendance_{student.id}')
                is_present = True if status == 'present' else False if status == 'absent' else None

                if is_present is not None:
                    # Avoid duplicate records
                    Attendance.objects.update_or_create(
                        student=student,
                        date=today,
                        defaults={'is_present': is_present}
                    )
                    marked_ids.append(student.id)

            # Mark unmarked students as absent
            unmarked_students = students.exclude(id__in=marked_ids)
            for student in unmarked_students:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'is_present': False}
                )

            return redirect('mark_attendance')

    return render(request, 'attendance_app/mark_attendance.html', {'students': students})

@login_required(login_url='/login/')
def attendance_report(request):
    section = request.GET.get('section')
    students = Student.objects.filter(section=section) if section else []

    # Get total distinct attendance days for this section
    if section:
        all_students_in_section = Student.objects.filter(section=section)
        all_attendance = Attendance.objects.filter(student__in=all_students_in_section)
        total_days = all_attendance.values('date').distinct().count()
    else:
        total_days = 0

    for student in students:
        present_count = Attendance.objects.filter(student=student, is_present=True).count()
        student.present_count = present_count
        student.total_days = total_days
        student.attendance_percent = round((present_count / total_days) * 100, 2) if total_days > 0 else 0

    return render(request, 'attendance_app/attendance_report.html', {
        'students': students,
        'section': section
    })


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

from django.shortcuts import get_object_or_404

def remove_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('add_student')  # or wherever you list students

@login_required(login_url='/login/')
def daywise(request):
    roll_number=request.POST.get('roll_number')
    student=None
    attendance_records=[]
    if roll_number:
        try:
            student=Student.objects.get(roll_number=roll_number)
            attendance_records=Attendance.objects.filter(student=student).order_by('date')
        except Student.DoesNotExist:
            student=None


    return render(request,'attendance_app/daywise.html', {
        'student':student,
        'attendance_records':attendance_records,
        'roll_number':roll_number
    })








#student login
from datetime import date
from django.contrib import messages

from .models import Student,StudentLogin


def student_login(request):
    if request.method == 'POST':
        name = request.POST['username']
        roll = request.POST['password']  # entered as password

        try:
            # Check if student exists in DB added by employee
            student_login = StudentLogin.objects.get(username=name, password=roll)
            request.session['student_id'] = student_login.student.id
            return redirect('student_dash')
        except StudentLogin.DoesNotExist:
            messages.error(request, "Invalid name or roll number")
            return redirect('login')  # back to login page

    return redirect('login')

def student_dash(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    
    return render(request, 'attendance_app/student_dash.html')


def student_dashboard(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')

    student = Student.objects.get(id=student_id)
    today = date.today()

    # Today's attendance
    attendance_today = Attendance.objects.filter(student=student, date=today).first()
    today_status = "Present" if attendance_today and attendance_today.is_present else "Absent"

    # Total & Present counts
    total_days = Attendance.objects.filter(student=student).values('date').distinct().count()
    days_present = Attendance.objects.filter(student=student, is_present=True).count()
    attendance_percent = round((days_present / total_days) * 100, 2) if total_days > 0 else 0

    return render(request, 'attendance_app/student_dashboard.html', {
        'student': student,
        'today': today.strftime('%d-%m-%Y'),
        'today_status': today_status,
        'total_days': total_days,
        'days_present': days_present,
        'attendance_percent': attendance_percent,
    })

def student_daywise(request):
    student_id = request.session.get('student_id')
    if not student_id:
        return redirect('login')
    #roll_number=request.POST.get('roll_number')
    student=None
    attendance_records=[]
    if student_id:
        try:
            student=Student.objects.get(id=student_id)
            attendance_records=Attendance.objects.filter(student=student).order_by('date')
        except Student.DoesNotExist:
            student=None


    return render(request,'attendance_app/student_daywise.html', {
        'student':student,
        'attendance_records':attendance_records,
        
    })



def student_logout(request):
    request.session.flush()  # Clear session data
    return redirect('login')  # Redirect to login page


from django.contrib import messages

def student_forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        new_password = request.POST['new_password']

        try:
            student_login = StudentLogin.objects.get(username=username)
            student_login.password = new_password
            student_login.save()
            messages.success(request, 'Password updated successfully! Please login.')
            return redirect('login')
        except StudentLogin.DoesNotExist:
            messages.error(request, 'Username not found.')
            return redirect('student_forgot_password')

    return render(request, 'attendance_app/sforgot.html')
