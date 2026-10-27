from django.db import models
from member.models import Member

class Event(models.Model):
    eno = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    etitle = models.CharField(max_length=10000)
    econtent = models.TextField()
    ehit = models.IntegerField(default=0)
    first_date = models.DateTimeField(auto_now=True,blank=True)
    end_date = models.DateTimeField(auto_now=True,blank=True)
    edate = models.DateTimeField(auto_now=True,blank=True)
    efile = models.ImageField(blank=True,upload_to='event')
    efile2 = models.ImageField(blank=True,upload_to='event')
    
    def __str__(self):
        return f'{self.eno},{self.etitle},{self.edate}'
