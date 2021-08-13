from django.urls import path, include

from . import views

urlpatterns = [
    #Leave as empty string for base url
	path('', views.home, name="home"),
	path('register', views.register, name="register"),
	path("login", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	path("doctor", views.doctor, name="doctor"),
	path("doctorDashboard", views.doctorDashboard, name="doctorDashboard"),
	path("doctorProfile", views.doctorProfile, name="doctorProfile"),
	path("doctorUpdateProfile", views.doctorUpdateProfile, name="doctorUpdateProfile"),
	path("doctorAppointments", views.doctorAppointments, name="doctorAppointments"),
	path("doctorsList", views.doctorsList, name="doctorsList"),
	path("patient", views.patient, name="patient"),
	path("patientDashboard", views.patientDashboard, name="patientDashboard"),
	path("searchResult", views.searchResult, name="searchResult"),
	path("doctor/<int:doctor_id>/", views.appointment, name="appointment"),
	path("prescription", views.prescription, name="prescription"),
]