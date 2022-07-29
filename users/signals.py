from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserAppointment, UserProfile
from datetime import datetime
import uuid


@receiver(post_save, sender=User)
def userprofile_signal(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff is False and instance.is_superuser is False:
            UserProfile.objects.create(reg_user=instance)
            
    
@receiver(pre_save, sender=UserProfile)
def generate_userid_signal(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace("-", "").upper()[:10]

@receiver(pre_save, sender=UserProfile)
def age_signal(sender, instance, **kwargs):    
    try:
        if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > instance.created.strftime('%Y-%m-%d %H:%M:%S'):
            userDob = str(instance.dob)
            strippedDob = datetime.strptime(userDob, '%Y-%m-%d')
            currentDate = datetime.now()
            userAge = currentDate - strippedDob
            calcAge = int(userAge.days/365.25)
            instance.age = calcAge
        else:
            userDob = str(instance.dob)
            strippedDob = datetime.strptime(userDob, '%Y-%m-%d')
            currentDate = datetime.now()
            userAge = currentDate - strippedDob
            calcAge = int(userAge.days/365.25)
            instance.age = calcAge
            
    except AttributeError:
        return

@receiver(pre_save, sender=UserAppointment)
def generate_appoint_id(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).upper().replace("-", "")[:8]
