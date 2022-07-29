from django.contrib.auth.models import User
from django.db import models
from PIL import Image
from traitlets import default


class UserProfile(models.Model):
    id = models.CharField(primary_key=True, unique=True, max_length=12, editable=False)
    reg_user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    profile_pic = models.ImageField(upload_to='UserDps/', default='default.jpg')
    gender = models.CharField(max_length=10, blank=False)
    location = models.CharField(max_length=50, blank=False)
    dob = models.DateField(null=True)
    age = models.PositiveIntegerField(default=0)
    phone_no = models.CharField(max_length=15, blank=False)
    marital_status = models.CharField(max_length=15, blank=False)
    
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.reg_user.username}'
    
    class Meta:
        verbose_name_plural = 'User Profiles'
        ordering = ['reg_user']
        
    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        
        resize_profile_img = Image.open(self.profile_pic.path)
        
        if resize_profile_img.height > 500 and resize_profile_img.width > 500:
            output_size = (500, 500)
            resize_profile_img.thumbnail(output_size)
            resize_profile_img.save(self.profile_pic.path)
    
            
class YourStory(models.Model):
    victim = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    experience = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.experience}'[:50]
    
    class Meta:
        verbose_name_plural = 'Experiences'
        ordering = ['victim', 'created']

    
class UserAppointment(models.Model):
    id = models.CharField(max_length=8, editable=False, primary_key=True)
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, editable=False)
    medic = models.CharField(max_length=150)
    appointment_date = models.DateField(blank=False)
    appointment_time = models.TimeField(blank=False)
    type_session = models.CharField(max_length=20, blank=False)
    duration = models.CharField(max_length=50, blank=False)
    company = models.CharField(max_length=10, blank=False)
    scheduled = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.medic}'

    class Meta:
        verbose_name_plural = 'Appointments'
        ordering = ['scheduled']
        

class AskQuestion(models.Model):
    questioner = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)
    question = models.TextField(blank=False)
    
    asked = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.question}'[:40]
    
    class Meta:
        verbose_name_plural = 'FAQs'
        ordering = ['asked']
        