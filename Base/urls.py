from django.urls import path
from django.http import HttpResponse
from .views import Contact, FeedBack, Appointment, Home, About, Bookings, Contact, FeedBack, DoctorAppointments, Profile, UpdatePassword, DoctorProfile,  AppointmentsExcel, AppointnmentPDF, SetBill, payment_successful, payment_cancelled

urlpatterns = [
    path('', Home, name= 'home'),
    path('about', About, name= 'about'),
    path('contact', Contact, name= 'contact'),
    path('feedback', FeedBack, name= 'feedback'),
    path('appointment', Appointment, name= 'appointment'),
    path('bookings', Bookings, name= 'bookings'),
    path('contact', Contact, name= 'contact'),
    path('feedback', FeedBack, name= 'feedback'),
    path('doctorAppointments', DoctorAppointments, name= 'doctor-appointments'),
    path('bill/<slug>', SetBill, name= 'bill'),
    path('profile', Profile, name= 'profile'),
    path('update-password/', UpdatePassword, name='update-password'),
    path('doctor/<int:id>/', DoctorProfile, name= 'doctor-profile'),
    path('pdf/<int:id>/', AppointnmentPDF, name='pdf'),
    path('excel/', AppointmentsExcel, name= 'appointments-excel'),
    path('payment-success/', payment_successful, name= 'bill-success'),
    path('payment-cancel/', payment_cancelled, name= 'bill-cancel'),
    # path('stripe_webhook/', stripe_webhook, name='stripe_webhook'),
]