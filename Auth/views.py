from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import Profile
from .forms import UserForm
from django.contrib import messages

# Create your views here.
def Login(request) : 
    if request.user.is_authenticated : 
        return redirect('home')
    
    if request.method == 'POST' : 
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request= request,username= username,password= password)

        if user is not None : 
            login(request, user)
            messages.success(request, 'User Logged In Successfully!')
            return redirect('home')
        else : 
            messages.error(request, "Invalid Credentials!")

    return render(request, 'login.html')

def Logout(request) : 
    logout(request)
    messages.success(request, 'User Logged Out Successfully!')
    return redirect('login')

def Register(request) : 
    if request.user.is_authenticated : 
        return redirect('home')
    
    form = UserForm()
    
    if request.method == 'POST' : 
        form = UserForm(request.POST)

        if form.is_valid() : 
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            gender = form.cleaned_data.get('gender')      

            user = authenticate(request= request, username= username, password= password)

            if user is not None : 
                login(request, user)

                profile = Profile.objects.create(user= request.user, gender= gender)
                
                if gender == 'male' : 
                    profile.image = 'prof_male.png'
                else :
                    profile.image = 'prof_female.png'

                profile.save()
                messages.success(request, "User Registered Successfully!")
                return redirect('home')
            else : 
                messages.error(request, "There's an error with the processing, please try again!")
        else : 
            messages.error(request, "Enter Details Correctly!")
    
    return render(request, 'register.html', {'form': form})