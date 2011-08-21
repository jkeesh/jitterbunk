from django.db import models
from django.contrib.auth.models import User

class Bunk(models.Model):
    bunker = models.ForeignKey(User, related_name="bunks_sent")
    bunkee = models.ForeignKey(User, related_name="bunks_received")
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    ## Constants to define bunk filters
    ALL         =   0
    SENT        =   1
    RECEIVED    =   2
        
    def __unicode__(self):
        return "%s bunked %s at %s" % (bunker, bunkee, created_at)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fbid = models.BigIntegerField(default=0, primary_key=True)
    friends = models.ManyToManyField("self")
    
    def bunk(self, other):
        bunk = Bunk(bunker=self, bunkee=other)
        bunk.save()
        
    def get_friends(self):
        return self.friends.all()
        
    def get_bunks(self, filter=Bunk.ALL):
        if filter == Bunk.ALL:
            sent = Bunk.objects.filter(bunker=self)
            received = Bunk.objects.filter(bunkee=self)
            return chain(sent, received)
        elif filter == Bunk.SENT:
            return Bunk.objects.filter(bunker=self)
        elif filter == Bunk.RECEIVED:
            return Bunk.objects.filter(bunkee=self)
    
    def unseen_count(self):
        return len(Bunk.objects.filter(bunkee=self, seen=False))
    
    
    def __unicode__(self):
        return "%s" % self.user
