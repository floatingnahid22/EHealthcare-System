from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *

# Create your views here.
# /----- Views for Homepage -----/
def home(request):
    return render(request, 'html/home.html')

# /----- Views for User Registration -----/
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        patient = request.POST['patient']


        if password == password_confirm:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username exist")
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.error(request, "This email is already used")
                return redirect('register')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                # usertype = userType(patient=patient, user=user)
                if patient == 'Patient':
                    usertype = userType.objects.create(user=user, patient=True)
                    usertype.save()
                    auth.login(request, user)
                    return redirect('patient')
                else:
                    usertype = userType.objects.create(user=user)
                    usertype.save()
                    auth.login(request, user)
                    return redirect('doctor')
                # auth.login(request, user)


                # messages.info(request, "User successfully created")
                # return redirect('register')
        else:
            messages.error(request, "Password not matching")
            return redirect('register')
    else:
        return render(request, 'html/register.html')


# /----- Views for User Login -----/
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # if user.usertype.patient == False:
            #     return redirect('doctor')
            # else:
            #     return redirect('patient')
            return redirect('/')
        else:
            messages.info(request, "Wrong username or password")
            return redirect('login')
    else:
        return render(request, 'html/login.html')


# /----- Views for User Logout -----/
def logout(request):
    auth.logout(request)
    return redirect('/')

def doctor(request):
    if request.method == 'POST':
        fullName = request.POST['fullName']
        designation = request.POST['designation']
        speciality = request.POST['speciality']
        degree = request.POST['degree']
        fees = request.POST['fees']
        visitingHours = request.POST['visitingHours']

        doctorinfo = doctorInfo(fullName=fullName, designation=designation, speciality=speciality, degree=degree, fees=fees,
                                visitingHours=visitingHours)
        if request.user.is_authenticated:
            user = request.user
            doctorinfo.user_id = user.id
            doctorinfo.save()
            messages.info(request, "Successfully submitted")
            return redirect('doctor')
    else:
        return render(request, 'html/doctor.html')

def doctorsList(request):
    doctors = doctorInfo.objects.all()

    context = {'doctors': doctors}
    return render(request, 'html/doctorsList.html', context)

def patient(request):
    return render(request, 'html/patient.html')