from django.conf import settings
from django.core.urlresolvers import reverse 
#from django_hosts.resolvers import reverse
from django.db import models
from .utils import code_generator, create_shortcode, add_url_prefix
from .validators import validate_url, validate_dot_com

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15) 

#Model Manager
class SrturlManager(models.Manager):
	def all(self, *args, **kwargs): #overwritting the all() method
		qs_main = super(SrturlManager, self).all(*args, **kwargs)
		qs = qs_main.filter(active=True)
		return qs

	def refresh_shortcodes(self, items=None):
		qs = Srturl.objects.filter(id__gte=1)
		if items is not None and isinstance(items,int):
			qs = qs.order_by('-id')[:items]
		new_codes = 0
		for q in qs:
			q.shortcode = create_shortcode(q)
			# print(q.id)
			q.save()
			new_codes +=1
		return "New codes made: {i}".format(i=new_codes)


#extending/inheriting from the model class
class Srturl(models.Model):
	url 			= models.URLField(max_length=220, validators=[validate_url]) #models.CharField(max_length=220, validators=[validate_url, validate_dot_com])
	shortcode 		= models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
	updated 		= models.DateTimeField(auto_now=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	active			= models.BooleanField(default=True)
	#empty_datetime  = models.DateTimeField(auto_now=False, auto_now_add=False)

	objects 		= SrturlManager()
	#some_randon     = SrturlManager()

	def save(self,*args, **kwargs):
		if (not self.shortcode): #self.shortcode is None or self.shortcode == ""
			self.shortcode = create_shortcode(self)
		self.url = add_url_prefix(self.url)
		# print('models url',self.url)
		super(Srturl, self).save(*args, **kwargs)

	# class Meta:
	# 	ordering = '-id'

	def __str__(self): #python3
		return str(self.url)

	def __unicode__(self): #python2
		return str(self.url)

	def get_short_url(self):
		url_path = reverse("scode", kwargs ={"shortcode": self.shortcode})
		#url_path = reverse("scode", kwargs ={"shortcode": self.shortcode}, host="www", scheme='http')
		return url_path   #{shortcode}".format(shortcode=self.shortcode)

	#def get_short_url(self):
		#return reverse('shortener:redirect', kwargs={'shortcode': self.shortcode})



















