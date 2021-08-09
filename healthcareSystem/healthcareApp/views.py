from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.db.models import Q

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
        designation = request.POST['designation']
        speciality = request.POST['speciality']
        degree = request.POST['degree']
        fees = request.POST['fees']
        visitingHours = request.POST['visitingHours']
        image = request.FILES['image']

        doctorinfo = doctorInfo(fullName=fullName, designation=designation, speciality=speciality, degree=degree, fees=fees,
                                visitingHours=visitingHours, image=image)
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
        bloodGroup = request.POST['bloodGroup']
        bloodPressure = request.POST['bloodPressure']

        patientinfo = patientInfo(fullName=fullName, address=address, phoneNumber=phoneNumber, DoB=DoB,
                                  age=age, bloodGroup=bloodGroup, bloodPressure=bloodPressure)
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
        appointments = Appointment.objects.all()
        appointments_count = appointments.count()

    context = {'doctor': doctor, 'appointments': appointments, 'appointments_count': appointments_count}
    return render(request, 'html/doctorDashboard.html', context)


# /----- Views for Patient Dashboard -----/
def patientDashboard(request):
    return render(request, 'html/patientDashboard.html')