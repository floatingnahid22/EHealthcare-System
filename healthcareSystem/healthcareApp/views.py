from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.db.models import Q
from datetime import date
from .filters import AppointmentFilter
from cryptography.fernet import Fernet


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


# /----- Views for Doctor Information Form -----/
def doctor(request):
    if request.method == 'POST':
        fullName = request.POST['fullName']
        mobile = request.POST['mobile']
        speciality = request.POST['speciality']
        degree = request.POST['degree']
        hospitalName = request.POST['hospitalName']
        fees = request.POST['fees']
        visitingHours = request.POST['visitingHours']
        image = request.FILES['image']

        doctorinfo = doctorInfo(fullName=fullName, mobile=mobile, speciality=speciality, degree=degree,
                                hospitalName=hospitalName, fees=fees, visitingHours=visitingHours, image=image)
        if request.user.is_authenticated:
            user = request.user
            doctorinfo.user_id = user.id
            doctorinfo.save()
            messages.info(request, "Successfully submitted")
            return redirect('doctor')
    else:
        return render(request, 'html/doctor.html')


# /----- Views for All Doctors List -----/
def doctorsList(request):
    doctors = doctorInfo.objects.all()

    context = {'doctors': doctors}
    return render(request, 'html/doctorsList.html', context)


# /----- Views for Patient Information Form -----/
def patient(request):
    if request.method == 'POST':
        fullName = request.POST['fullName']
        address = request.POST['address']
        phoneNumber = request.POST['phoneNumber']
        DoB = request.POST['DoB']
        age = request.POST['age']
        gender = request.POST['gender']
        bloodGroup = request.POST['bloodGroup']
        bloodPressure = request.POST['bloodPressure']

        patientinfo = patientInfo(fullName=fullName, address=address, phoneNumber=phoneNumber, DoB=DoB,
                                  age=age, gender=gender, bloodGroup=bloodGroup, bloodPressure=bloodPressure)

        if request.user.is_authenticated:
            user = request.user
            patientinfo.user_id = user.id
            patientinfo.save()
            messages.info(request, "Thank You, Successfully submitted")
            return redirect('patient')
    else:
        return render(request, 'html/patient.html')


# /----- Views for Search -----/
def searchResult(request):
    if request.method == "GET":
        searched = request.GET.get('searched')
        result = doctorInfo.objects.all().filter(Q(fullName__icontains=searched) | Q(speciality__icontains=searched))

        context = {'result': result, 'searched': searched}
        return render(request, 'html/searchResult.html', context)
    else:
        return render(request, 'html/searchResult.html')


# /----- Views for Appointment -----/
def appointment(request, doctor_id):
    doctors = doctorInfo.objects.get(pk=doctor_id)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        date = request.POST['date']
        timeSlot = request.POST['timeSlot']

        appointmentinfo = Appointment(name=name, phone=phone, email=email, date=date, timeSlot=timeSlot)
        if request.user.is_authenticated:
            user = request.user
            appointmentinfo.user_id = user.id
            appointmentinfo.doctor = doctors
            appointmentinfo.save()
            return redirect('/')
    else:
        return render(request, 'html/appointment.html')

    context = {'doctors': doctors}
    return render(request, 'html/appointment.html', context)


# /----- Views for Doctor Dashboard -----/
def doctorDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        doctor = doctorInfo.objects.get(user=user)
        appointments = doctor.appointment_set.filter(date=date.today()).order_by('date')
        appointments_count = appointments.count()
        myFilter = AppointmentFilter(request.GET, queryset=appointments)
        appointments = myFilter.qs

    context = {'doctor': doctor, 'appointments': appointments, 'appointments_count': appointments_count, 'myFilter': myFilter}
    return render(request, 'html/doctorDashboard.html', context)


# /----- Views for DashBoard | Doctor All Appointments -----/
def doctorAppointments(request):
    if request.user.is_authenticated:
        user = request.user
        doctor = doctorInfo.objects.get(user=user)
        appointments = doctor.appointment_set.all().order_by('date')
        appointments_count = appointments.count()
        myFilter = AppointmentFilter(request.GET, queryset=appointments)
        appointments = myFilter.qs

    context = {'doctor': doctor, 'appointments': appointments, 'appointments_count': appointments_count,
               'myFilter': myFilter}
    return render(request, 'html/doctorAppointments.html', context)


# /----- Views for Dashboard | Doctor Profile -----/
def doctorProfile(request):
    if request.user.is_authenticated:
        user = request.user
        doctor = doctorInfo.objects.get(user=user)

    context = {'doctor': doctor}
    return render(request, 'html/doctorProfile.html', context)


# /----- Views for Doctor Update Profile -----/
def doctorUpdateProfile(request):
    if request.user.is_authenticated:
        user = request.user
        doctor = doctorInfo.objects.get(user=user)

        if request.method == 'POST':
            doctor = doctorInfo(request.POST, request.FILES or None)
            # fullName = request.POST['fullName']
            # mobile = request.POST['mobile']
            # speciality = request.POST['speciality']
            # degree = request.POST['degree']
            # hospitalName = request.POST['hospitalName']
            # fees = request.POST['fees']
            # visitingHours = request.POST['visitingHours']
            # image = request.FILES['image']

            profile_qs = doctorInfo.objects.filter(user=request.user)
            if profile_qs.exists():
                profile_qs.update(user=request.user, fullName=request.POST['fullName'], mobile=request.POST['mobile'],
                                  speciality=request.POST['speciality'],
                              degree=request.POST['degree'], hospitalName=request.POST['hospitalName'],
                                  fees=request.POST['fees'], visitingHours=request.POST['visitingHours'],
                              image=request.FILES['image'])
            else:
                doctorInfo.objects.create(user=request.user, fullName=request.POST['fullName'], mobile=request.POST['mobile'],
                                  speciality=request.POST['speciality'],
                              degree=request.POST['degree'], hospitalName=request.POST['hospitalName'],
                                  fees=request.POST['fees'], visitingHours=request.POST['visitingHours'],
                              image=request.FILES['image'])

                return redirect('doctorProfile')


    return render(request, 'html/doctorUpdateProfile.html', {'doctor': doctor})


# /----- Views for Patient Dashboard -----/
def patientDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        patient = patientInfo.objects.get(user=user)

    context = {'patient': patient}
    return render(request, 'html/patientDashboard.html', context)


def prescription(request):
    return render(request, 'html/prescription.html')