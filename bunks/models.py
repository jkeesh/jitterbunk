from django.db import models
from django.contrib.auth.models import User

class Bunk(models.Model):
    bunker = models.ForeignKey(User, related_name="bunks_sent")
    bunkee = models.ForeignKey(User, related_name="bunks_received")
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s bunked %s at %s" % (bunker, bunkee, created_at)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fbid = models.BigIntegerField(default=0, primary_key=True)
    friends = models.ManyToManyField("self")
    
    def __unicode__(self):
        return "%s" % self.user
