from django.db import models
from shortener.models import Srturl

class ClickEventManager(models.Manager):
	def create_event(self, instance):
		if isinstance(instance, Srturl):
			obj, created = self.get_or_create(srt_url=instance)
			obj.count += 1
			obj.save()
			return obj.count
		return None

class ClickEvent(models.Model):
	srt_url 		= models.OneToOneField(Srturl)
	count 			= models.IntegerField(default=0)
	updated 		= models.DateTimeField(auto_now=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects			= ClickEventManager()

	def __str__(self): #python3
		return '{i}'.format(i=self.count)

	def __unicode__(self): #python2
		return '{i}'.format(i=self.count)