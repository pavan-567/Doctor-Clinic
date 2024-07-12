from io import BytesIO

import pandas as pd
import stripe
from Auth.models import Profile as UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from xhtml2pdf import pisa
from django.conf import settings

from .models import Appointment as Appt
from .models import Bill, Doctor, Response


# Create your views here.
def Home(request) : 
    return render(request, 'home.html')

def About(request) : 
    doctors = Doctor.objects.all()
    return render(request, 'about.html', {'doctors': doctors})

def Contact(request) : 
    if request.method == "POST" : 
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Response.objects.create(name= name, email= email, message= message, type= 'contact')
        messages.success(request, "Thank you for contacting us! Your details have been received successfully.. We'll Review and Hit Back To You Soon!")
        # return redirect('home')

    return render(request, 'response.html', {'mode': 'contact'})

def FeedBack(request) :
    if request.method == "POST" : 
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Response.objects.create(name= name, email= email, message= message, type= 'feedback')
        messages.success(request, "Thank You For The Feedback!")
        # return redirect('home')
    
    return render(request, 'response.html', {'mode' : 'feedback'})

def Appointment(request) :  
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')

    if request.method == 'POST' and request.user.is_authenticated : 
        doctor = Doctor.objects.get(id= request.POST.get('doctor-select'))
        appDate = request.POST.get('appointment-date')
        # appTime = datetime.strptime(request.POST.get('appointment-time'), '%I:%M %p').time()
        appTime = request.POST.get('appointment-time')
        patientName = request.POST.get('patient-name')
        patientEmail = request.POST.get('patient-email')
        patientProblem = request.POST.get('problem')
        patientLocation = request.POST.get('location')
        City = request.POST.get('city')
        State = request.POST.get('state') 
        ZipCode = request.POST.get('code')
        consult = request.POST.get('consult')
        phone = request.POST.get('phone')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        gender = request.POST.get('gender')
        age = request.POST.get('age')

        appointmentInfo = {
            'user': request.user,
            'doctor': doctor,
            'date': appDate,
            'time': appTime,
            'patientName': patientName,
            'patientEmail' : patientEmail,
            'patientProblem' : patientProblem,
            'patientLocation' : patientLocation,
            'patientCity' : City,
            'patientState' : State,
            'postalCode' : ZipCode,
            'consultStatus' : consult,
            'phone' : phone,
            'patientHeight' : height,
            'patientWeight' : weight,
            'patientGender' : gender,
            'patientAge' : age
        }

        # Appt.objects.create(user= request.user, doctor = doctor, date= appDate, time= appTime, patientName= patientName, patientEmail= patientEmail, patientProblem= patientProblem, patientLocation= patientLocation, patientCity= City, patientState= State, postalCode= ZipCode, consultStatus= consult, phone=phone)
        Appt.objects.create(**appointmentInfo)  

        messages.success(request, "Appointment booked successfully!")

        return redirect('bookings')
    
    # UserProfiles = UserProfile.objects.filter(role= 'doctor')
    if category: 
        doctors = Doctor.objects.filter(speciality= category)
    elif search : 
        doctors = Doctor.objects.filter(user__username__icontains= search)
    else : 
        doctors = Doctor.objects.all()
    categories = Doctor.objects.values_list('speciality')
    return render(request, 'appointment.html', {'doctors': doctors, 'categories' : categories.distinct(), 'category': category, 'search': search})


# TODO: PAYMENT
def Bookings(request) : 
    if not request.user.is_authenticated : 
        return redirect('login')
    
    if request.method == "POST" : 
        appointmentId = request.POST.get('appointmentId')
        appointment = Appt.objects.get(id= appointmentId)
        stripe.api_key = 'sk_test_51OkSw4SClaubPB0OptdiUatOTgP49DnNUGixB6XbG79xKVhmmQcrHvmYNe2R3AiNmiXLxoiZpig1dftzYTqWyvvJ00J3zCArhq'
        checkout_session = stripe.checkout.Session.create(
            payment_method_types= ['card'],
            line_items= [
                {
                 'price_data' : {
                   'currency' : 'usd', 
                   'unit_amount' : int(appointment.bill.totalBill) * 100,
                   'product_data': {
                       'name' : f'{appointment.user.username}\'s Bill',
                       'description' : f'{appointment.bill.billDescription}',
                       
                   }
                 },
                 'quantity': 1 
                }],
            mode= 'payment',
            customer_creation= 'always',
            success_url= 'http://localhost:8000' +reverse('bill-success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url= 'http://localhost:8000' + reverse('bill-cancel')
        )
        return redirect(checkout_session.url, code=303)
    
    userAppointments = Appt.objects.filter(user= request.user).order_by('created_at')
    return render(request, 'bookings.html', {'bookings' : userAppointments})


def DoctorAppointments(request) : 
    if not request.user.is_authenticated or not request.user.profile.role == 'doctor' : 
        return redirect('login')
    
    if request.method == "POST" : 
        status = request.POST.get('status')
        appointmentId = request.POST.get('doctor-appointment')
        confirmation = request.POST.get('confirmation')

        appointment = Appt.objects.get(id= appointmentId)
        appointment.status = status
        if confirmation is not None : 
            appointment.patientApproved = confirmation
            appointment.save()
        if confirmation == 'accept' : 
            try : 
                Bill.objects.get(appointment= appointment)
            except :
                print("ERROR ME AAYA BHAI!!")
                Bill.objects.create(
                    user= appointment.user,
                    appointment= appointment
                )
        messages.success(request, "Updated The Details")
  
    
    # 1. Get Doctor
    doctor = Doctor.objects.get(user= request.user)

    # 2. Get Appointments
    appointments = Appt.objects.filter(doctor= doctor)

    return render(request, 'doctorAppointments.html', {'appointments': appointments})


def Profile(request) :
    if not request.user.is_authenticated :  
        return redirect('login')
    
    if request.method == "POST" : 

        image = request.FILES.get('profile-pic')
        username = request.POST.get('username')
        email = request.POST.get('email')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        gender = request.POST.get('gender')

        user = request.user 
        profile = UserProfile.objects.get(user= user)


        user.username = username
        user.email = email
        user.first_name = firstName
        user.last_name = lastName
        
        if image is not None : 
            profile.image = image 
        profile.gender = gender

        messages.success(request, "Updated Profile Details Successfully")

        user.save()
        profile.save()

    return render(request, 'profile.html')


def UpdatePassword(request) : 
    if not request.user.is_authenticated or request.method == 'GET' : 
        return redirect('profile')

    oldPass = request.POST.get('pass-old')
    newPass = request.POST.get('pass-new')
    cnfPass = request.POST.get('pass-cnf')



    user = request.user

    if user.check_password(oldPass) :
        if newPass == cnfPass : 
            user.set_password(newPass)
            user.save()
            messages.success(request, "Password updated successfully")

    return redirect('login')

def DoctorProfile(request, id) :
    doctor = Doctor.objects.get(id= id) 
    return render(request, 'doctor.html', {'doctor': doctor})



def SetBill(request, slug) : 
    bill = Bill.objects.get(slug= slug)

    if request.method == "POST" : 
        totalAmnt = request.POST.get('total', 0)
        description = request.POST.get('description', '')
        bill.totalBill = totalAmnt
        bill.billDescription = description
        bill.save()
        return redirect('doctor-appointments')

    return render(request, 'bill.html', {'bill': bill})




# def AppointmentPdf(request) : 
#     doctors = Doctor.objects.all()
#     template_path = 'pdf/appointments.html'
#     context = {'doctors': doctors}

#     response = HttpResponse(content_type= 'application/pdf')
#     response['Content-Disposition'] = 'filename="appointments.pdf"'
    
#     template = get_template(template_path)
#     html = template.render(context)

#     pisa_status = pisa.CreatePDF(
#         html,
#         dest= response
#     )

#     if pisa_status.err : 
#         return HttpResponse('We Have Sm Errs <pre>' + html + '</pre>')
#     return response

def AppointnmentPDF(request, id) :
    appointment = Appt.objects.get(id= id)
    print(appointment)
    template = 'pdf/appointment.html'
    context = {'appointment' : appointment}
    response = HttpResponse(content_type= 'application/pdf')
    filename = f"{appointment.patientName}-appointment"
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    template = get_template(template)
    html = template.render(context)
    result = BytesIO()
    pisa_status = pisa.CreatePDF(
    html,
    dest= response)
    # pisa_status = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pisa_status.err : 
        return HttpResponse('We Have Sm Errs <pre>' + html + '</pre>')
    # return HttpResponse(result.getvalue(), content_type= 'application/pdf')
    return response
   



def AppointmentsExcel(request) : 
    if not request.user.is_authenticated : 
        return redirect('login')
    
    appointments = Appt.objects.filter(user= request.user)
    appointmentData = []

    # Columns : Patient Name, Patient Email Doctor DateofAppt TimeofAppt Status
    for appointment in appointments : 

        totalBill = None 
        billPay = None 
        stripeId = None
        if appointment.patientApproved == 'accept' : 
            totalBill = appointment.bill.totalBill 
            billPay = "Paid" if appointment.bill.payBill == True else "Not Paid"
            stripeId = "---" if appointment.bill.stripeId == None else appointment.bill.stripeId
        appointmentData.append([
            appointment.patientName,
             appointment.patientEmail,
             appointment.patientProblem,
             appointment.patientLocation,
             appointment.patientCity,
             appointment.patientState,
             appointment.doctor.user,
             appointment.consultStatus,
             appointment.date,
             appointment.time,
             appointment.status,
             appointment.patientApproved,
             totalBill,
             billPay,
             stripeId
        ])


    df = pd.DataFrame(appointmentData, columns= ['Patient Name', 'Patient Email', 'Patient Problem', 'Patient Location', 'Patient City', 'Patient State', 'Doctor', 'Consult Mode', 'Date Of Appointment', 'Time Of Appointment', 'Status Of Appointment', 'Patient Approval Status', 'Total Bill', 'Bill Payment Status', 'Payment ID'])
    # df.to_excel('output.xlsx')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{request.user.username}-appointments.xlsx"'                                        
    df.to_excel(response)
    return response


# Payment Gateway
def payment_successful(request) : 
    stripe.api_key = 'sk_test_51OkSw4SClaubPB0OptdiUatOTgP49DnNUGixB6XbG79xKVhmmQcrHvmYNe2R3AiNmiXLxoiZpig1dftzYTqWyvvJ00J3zCArhq'
    checkout_session_id= request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    bill = Bill.objects.filter(user= request.user).order_by('-created_at').first()
    bill.stripeId = checkout_session_id
    bill.payBill = True
    bill.save()
    messages.success(request, f'payment of ${bill.totalBill} paid successfully!')
    return redirect('bookings')

def payment_cancelled(request) : 
    messages.error(request, 'Payment Failed! Please Retry Again!')
    return redirect('bookings')


# Not Needed Now

# @csrf_exempt
# def stripe_webhook(request):
#     stripe.api_key = 'sk_test_51OkSw4SClaubPB0OptdiUatOTgP49DnNUGixB6XbG79xKVhmmQcrHvmYNe2R3AiNmiXLxoiZpig1dftzYTqWyvvJ00J3zCArhq'
#     time.sleep(10)
#     payload = request.body
#     signature_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None 
#     try : 
#         event = stripe.Webhook.construct_event(
#             payload= payload,
#             sig_header= signature_header,
#             secret= 'sk_test_51OkSw4SClaubPB0OptdiUatOTgP49DnNUGixB6XbG79xKVhmmQcrHvmYNe2R3AiNmiXLxoiZpig1dftzYTqWyvvJ00J3zCArhq'
#         )
#     except ValueError as e : 
#         return HttpResponse(status= 400)
#     except stripe.error.SignatureVerificationError as e : 
#         return HttpResponse(status= 400)
#     if event['type'] == 'checkout.session.completed' : 
#         session = event['data']['object']
#         session_id = session.get('id', None)
#         time.sleep(15)
#         bill = Bill.objects.get(stripeId= session_id)
#         bill.payBill = True
#         bill.save()
#     return HttpResponse(status= 200)