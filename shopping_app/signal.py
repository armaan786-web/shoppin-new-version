from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from shopping_app.models import Profile



@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwargs):
    if created: 
        Profile.objects.create(user=instance)


@receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    try:
        instance.profile.save()
    except:
        pass
    
    


