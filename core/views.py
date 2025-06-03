from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'Student_AMS/index.html')

def about(request):
    return render(request, 'Student_AMS/about.html')

def contact(request):
    return render(request, 'Student_AMS/contact.html')

def department(request):
    return render(request, 'Student_AMS/departments.html')

def login(request):
    return render(request, 'Student_AMS/login.html')

def signup(request):
    return render(request, 'Student_AMS/signup.html')

def forgotPassword(request):
    return render(request, 'Student_AMS/forgotPassword.html')

def custom_404_view(request, exception):
    return render(request, 'Student_AMS/404.html', status=404)
