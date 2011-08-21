from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fbid = models.BigIntegerField(default=0, primary_key=True)
    friends = models.ManyToManyField("self")
    
    def __unicode__(self):
        return "%s" % self.user
