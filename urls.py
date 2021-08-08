from django.urls import path, include

from . import views

urlpatterns = [
    #Leave as empty string for base url
	path('', views.home, name="home"),
	path('register', views.register, name="register"),
	path("login", views.login, name="login"),
	path("logout", views.logout, name="logout"),
	path("doctor", views.doctor, name="doctor"),
	path("doctorsList", views.doctorsList, name="doctorsList"),
	path("patient", views.patient, name="patient"),
	path("patientlist", views.patientlist, name="patientlist"),

]