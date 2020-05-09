from django.db import models
from django.utils import timezone
from django.http import HttpResponse, JsonResponse

# Create your models here.
class Device(models.Model):
	title = models.CharField(max_length=250,null=False,unique=True)
	ipaddress = models.CharField(max_length=25, null=False)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	connected = models.BooleanField(default=True)
	last_seen= models.DateTimeField(null=True,blank=True)
	def get_pd_enabled(self):

	    queryset = Value.objects.get(device_id=self.id)
	    labels = []
	    data = []
	    queryset = Value.objects.filter()
	    for city in queryset:
	        labels.append(city.last_measured_moisture)
	        date= str((city.last_measured).strftime("%Y/%m/%dT%H:%M:00"))
	        data.append(date)
	    return labels,data

class Setup(models.Model):
  time_1 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_2 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  device_id = models.ForeignKey(
      Device, on_delete=models.CASCADE, related_name='blog_posts',primary_key=True)
  time_3 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_4 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_5 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_6 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_7 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_8 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_9 =  models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
  time_10 = models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)

  setupcompleted = models.BooleanField(default=False)

class Zone(models.Model):
  name = models.CharField(max_length=250,null=False,unique=True)
  device_id = models.ForeignKey(
      Device, on_delete=models.CASCADE, related_name='device_zone',primary_key=True)
  gpio = models.CharField(max_length=2,null=False)
  min_moisture =  models.IntegerField(null=True,blank=True)
  time_period =  models.IntegerField()
  last_measured = models.DateTimeField(null=True,blank=True)

  last_measured_moisture= models.IntegerField(null=True,blank=True)

  last_active_measured = models.DateTimeField(null=True,blank=True)
  last_active_moisture=  models.IntegerField(null=True,blank=True)
  setupcompleted = models.BooleanField(default=False)
  monitoring = models.BooleanField(default=False)


class Value(models.Model):
  device_id = models.ForeignKey(
      Device, on_delete=models.CASCADE, related_name='device_value')

  last_measured = models.DateTimeField(null=True,blank=True)

  last_measured_moisture= models.IntegerField(null=True,blank=True)
