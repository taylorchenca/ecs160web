from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfile(models.Model):
    user   = models.OneToOneField(User)
    picture = models.ImageField(upload_to="images")
    REQUIRED_FIELDS = ('user', 'email',)
    
    def __unicode__(self):
        return self.user.username
    
