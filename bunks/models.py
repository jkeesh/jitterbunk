from django.db import models
from django.contrib.auth.models import User

class UserMethods:
    """
    This class adds some additional convenience methods onto the User
    class.
    """
    def name(self):
        """
        Get the users full name
        """
        return self.first_name + " " + self.last_name
        
User.__bases__ += (UserMethods,)

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
        return "%s bunked %s at %s" % (self.bunker, self.bunkee, self.created_at)

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    fbid = models.BigIntegerField(default=0, primary_key=True)
    friends = models.ManyToManyField("self")
    
    def get_ratio(self):
        sent_count = self.get_bunks(Bunk.SENT).count()
        received_count = self.get_bunks(Bunk.RECEIVED).count()
        if received_count == 0:
            return 0 if sent_count == 0 else 'Inf'
        ratio = float(sent_count) / received_count
        return round(ratio, 2)
    
    def bunk(self, other):
        if self != other:
            bunk = Bunk(bunker=self.user, bunkee=other)
            bunk.save()
        
    def get_friends(self):
        return self.friends.all()
        
    def get_bunks(self, filter=Bunk.ALL):
        if filter == Bunk.ALL:
            sent = Bunk.objects.filter(bunker=self.user).order_by('-created_at')
            received = Bunk.objects.filter(bunkee=self.user).order_by('-created_at')
            return chain(sent, received)
        elif filter == Bunk.SENT:
            return Bunk.objects.filter(bunker=self.user).order_by('-created_at')
        elif filter == Bunk.RECEIVED:
            return Bunk.objects.filter(bunkee=self.user).order_by('-created_at')
    
    def unseen_count(self):
        return len(Bunk.objects.filter(bunkee=self.user, seen=False))
    
    
    def __unicode__(self):
        return "%s" % self.user
