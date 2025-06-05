from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.hashers import make_password
import json

# Login view
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# Home view with student listing
@login_required
def home(request):
    students = Student.objects.all()
    return render(request, 'home.html', {'students': students})

def forgot_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        user = CustomUser.objects.filter(username=username, security_question=question, security_answer=answer).first()
        if user:
            return redirect('reset_password', username=username)
        else:
            messages.error(request, 'Invalid security details')
    
    return render(request, 'forgot_password.html')


def reset_password(request, username):
    user = CustomUser.objects.get(username=username)
    if request.method == 'POST':
        password = request.POST.get('password')
        user.password = make_password(password)
        user.save()
        messages.success(request, 'Password reset successfully. Please log in.')
        return redirect('login')
    return render(request, 'reset_password.html', {'username': username})


# Add student view
@csrf_exempt
@login_required
def add_student(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        marks = int(request.POST.get('marks'))

        # Check if student with same name + subject exists
        existing = Student.objects.filter(name=name, subject=subject).first()

        if existing:
            existing.marks = F('marks') + marks
            existing.save()
            messages.success(request, 'Existing student found. Marks updated.')
        else:
            Student.objects.create(name=name, subject=subject, marks=marks)
            messages.success(request, 'New student added.')

    return redirect('home')

# Edit student view
@csrf_exempt
@login_required

def edit_student(request, id):
    print("Edit view hit")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student = Student.objects.get(id=id)
            student.name = data.get('name')
            student.subject = data.get('subject')
            student.marks = int(data.get('marks'))
            student.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'invalid method'}, status=405)

@csrf_exempt
def edit_student(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        from .models import Student
        student = Student.objects.get(id=id)
        student.name = data['name']
        student.subject = data['subject']
        student.marks = data['marks']
        student.save()
        return JsonResponse({'status': 'updated'})
    return JsonResponse({'status': 'fail'}, status=400)
# Delete student view
@login_required
def delete_student(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        return redirect('home')
    except Student.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Student not found'}, status=404)
