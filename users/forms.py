from users.models import AskQuestion, UserProfile, YourStory, UserAppointment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        
        self.fields['username'].label = 'Enter your name'
        self.error_messages['invalid_login'] = 'Please enter a correct name (include first name and surname) and password. Note that both fields may be case-sensitive.'

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter your first name ...', 'class': 'mt-2'}))
    last_name = forms.CharField(required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter your surname ...', 'class': 'mt-2'}))
    email = forms.EmailField(required=True, label='', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address ...', 'class': 'mt-2 mb-2'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Enter the same password as before for verification'}))
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class UpdateProfileForm(forms.ModelForm):
    choice_gender = (
        (None, '-- Select your gender --'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    choice_marital = (
        (None, '-- select marital status --'),
        ('Dating', 'Dating'),
        ('Engaged', 'Engaged'),
        ('Married', 'Married'),
    )
    
    gender = forms.ChoiceField(label='', widget=forms.Select(attrs={'type': 'select', 'class': 'mt-2 mb-2'}), choices=choice_gender)
    dob = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'date'}), help_text='Enter your date of birth')
    location = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'text', 'class': 'mt-2 mb-2', 'placeholder': 'Enter your county/location'}))
    phone_no = forms.CharField(label='', widget=forms.TextInput(attrs={'type': 'tel', 'class': 'mb-2', 'placeholder': 'Enter your mobile no.'}))
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'mb-3'}), label='Upload profile picture')
    marital_status = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select'}), label='', choices=choice_marital)
        
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'gender', 'dob', 'location', 'phone_no', 'marital_status']
        
        
class EditProfileForm(forms.ModelForm):
    choice_marital = (
        (None, '-- select marital status --'),
        ('Dating', 'Dating'),
        ('Engaged', 'Engaged'),
        ('Married', 'Married'),
    )
    profile_pic = forms.ImageField(widget=forms.FileInput(attrs={'class':'mb-3'}), label='Upload profile picture')
    marital_status = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select'}), choices=choice_marital)

    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'marital_status']


class ScheduleAppointmentForm(forms.ModelForm):
    choice_session = (
        (None, '-- choose session -- '),
        ('Physical', 'Physical'),
        ('Virtual', 'Virtual')
    )
    choice_duration = (
        (None, '-- select timeline -- '),
        ('Began Recently', 'Began Recently'),
        ('1 week', '1 week'),
        ('2 weeks', '2 weeks'),
        ('3 weeks', '3 weeks'),
        ('Month', 'Month'),
        ('More than a month', 'More than a month'),
        ('More than a year', 'More than a year'),
    )
    choice_company = (
        (None, '-- Select your choice -- '),
        ('Yes', 'Yes'),
        ('No', 'No'),        
    )
    
    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date', 'class': 'col-md-6'}))
    appointment_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time', 'class': 'col-md-6'}))
    type_session = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select'}), choices=choice_session)
    duration = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select'}), choices=choice_duration, help_text='For how long have you been a victim of Gender Based Violence (GBV)')
    company = forms.ChoiceField(widget=forms.Select(attrs={'type': 'select'}), label='Accompanied', choices=choice_company, help_text='Will you be accompanied?')
    
    class Meta:
        model = UserAppointment
        exclude = ['id']

class ShareExperienceForm(forms.ModelForm):
    experience = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Share your experience....'}), label='', required=True, help_text='You can include how long you endured GBV and how you dealt with')
    class Meta:
        model = YourStory
        fields = ['experience']
        
        
class HelpForm(forms.ModelForm):
    question = forms.CharField(widget=forms.Textarea(attrs = {"placeholder": 'Type your question here ...'}), label='', required=True)
    class Meta:
        model = AskQuestion
        fields = ['question']