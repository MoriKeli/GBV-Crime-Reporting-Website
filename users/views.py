from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import HelpForm, LoginForm, SignUpForm, UpdateProfileForm, EditProfileForm, ShareExperienceForm, ScheduleAppointmentForm
from .models import UserAppointment, UserProfile, YourStory


class UserLogin(LoginView):
    authentication_form = LoginForm
    template_name = 'users/login.html'
    

def signup_view(request):
    signupForm = SignUpForm()
    
    if request.method == 'POST':
        signupForm = SignUpForm(request.POST)
        
        if signupForm.is_valid():
            reguser = signupForm.save(commit=False)
            reguser.username = reguser.first_name + ' ' + reguser.last_name
            reguser.is_staff = False
            reguser.save()

            messages.success(request, 'Account created successfully')
            return redirect('user_profile')
        
    context = {'signup_form': signupForm} 
    return render(request, 'users/signup.html', context)

@login_required(login_url='user_login')
def userProfile_view(request):
    update_form = UpdateProfileForm(instance=request.user.userprofile)
    edit_form = EditProfileForm(instance=request.user.userprofile)
    
    if request.method == 'POST':
        update_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        edit_form = EditProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if update_form.is_valid():
            update_form.save()
            messages.info(request, 'Profile updated successfully!')
        
        elif edit_form.is_valid():
            edit_form.save()
            messages.info(request, 'Profile edited successfully!')
        
        return redirect('user_profile')
    
    context = {'update_form': update_form, 'edit_form': edit_form}
    return render(request, 'users/profile.html', context)


@login_required(login_url='user_login')
def homepage_view(request):
    scheduled_sessions = UserAppointment.objects.filter(patient=request.user.userprofile).all()
    
    context = {'appointments': scheduled_sessions}
    return render(request, 'users/homepage.html', context)


@login_required(login_url='user_login')
def medical_support_view(request):
    med_form = ScheduleAppointmentForm()
    
    if request.method == 'POST':
        med_form = ScheduleAppointmentForm(request.POST)
        if med_form.is_valid():
            med = med_form.save(commit=False)
            
            filter_schedules = UserAppointment.objects.filter(medic=med.medic, appointment_date=med.appointment_date, appointment_time=med.appointment_time).exists()
            if filter_schedules is True:
                messages.warning(request, f'{med.medic} has a scheduled appointment at the provided date & time. Kindly reschedule.')
            
            else:
                med.patient = request.user.userprofile
                med.save()
                messages.success(request, 'Appointment submitted successfully!')
                return redirect('medic')
    
    context = {'schedule_form': med_form}
    return render(request, 'users/medical-support.html', context)


@login_required(login_url='user_login')
def join_meeting_view(request):
    
    
    return render(request, 'users/meeting.html')


@login_required(login_url='user_login')
def scheduled_apppointments_view(request):
    user_scheduled_sessions = UserAppointment.objects.filter(patient=request.user.userprofile).order_by('scheduled')
    
    context = {'sessions': user_scheduled_sessions}
    return render(request, 'users/sessions.html', context)


@login_required(login_url='user_login')
def contact_us_view(request, name, location):
    medic_info = User.objects.get(username=name)
    location = medic_info.userprofile.location
    
    context = {'med': medic_info}
    return render(request, 'users/contact-us.html', context)


@login_required(login_url='user_login')
def testimonials_view(request):
    form = ShareExperienceForm()
    if request.method == 'POST':
        form = ShareExperienceForm(request.POST, )
        
        if form.is_valid():
            share = form.save(commit=False)
            share.victim = request.user.userprofile
            share.save()
            
            messages.success(request, 'Your story was submitted successfully!')
            return redirect('testimonials')
    
    
    testimonials = YourStory.objects.filter(victim__location__contains=request.user.userprofile.location).all()
    context = {'form': form, 'testimonials': testimonials}
    return render(request, 'users/testimonials.html', context)

@login_required(login_url='user_login')
def faq_view(request):
    quiz_form = HelpForm()
    if request.method == 'POST':
        quiz_form = HelpForm(request.POST)
        if quiz_form.is_valid():
            qf = quiz_form.save(commit=False)
            qf.questioner = request.user.userprofile
            qf.save()
            
            messages.success(request, 'Question submitted successfully!')
            return redirect('faq')
    
    context = {'faq_form': quiz_form}
    return render(request, 'users/faq.html', context)


class LogoutUser(LogoutView):
    template_name = 'users/logout.html'
    