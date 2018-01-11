from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.conf import settings
from analytics.models import ClickEvent
from .forms import SubmitUrlForm
from .models import Srturl
from .utils import add_url_prefix


class HomeView(View):
	def get(self, request, *args, **kwargs):
		the_form = SubmitUrlForm()
		bg_image = 'https://interfacelift.com/wallpaper/7yz4ma1/04122_eno_1440x900.jpg'
		context = {
			"title": "Srturl",
			"form": the_form,
			"bg_image": bg_image,
		}
		return render(request, "shortener/home.html", context)
	
	def post(self, request , *args, **kwargs):
		#url = request.POST.get('url') # better than request.POST[url], will return None instead of error
		# ShortUrl, created = Srturl.objects.get_or_create(url=url)
		# REDIRECT_URL = settings.DEFAULT_REDIRECT_URL+ '/' + ShortUrl.shortcode
		# context = {"REDIRECT_URL": REDIRECT_URL}
		# bg_image = "https://interfacelift.com/wallpaper/7yz4ma1/04136_therockatrainier_1440x900.jpg"
		bg_image = 'https://interfacelift.com/wallpaper/7yz4ma1/04101_minimalmountains_1440x900.jpg'
		form = SubmitUrlForm(request.POST)
		context = {
			"title": "Srturl",
			"form": form,
			"bg_image": bg_image,
		}
		template = "shortener/home.html"

		if form.is_valid():
			url = form.cleaned_data.get("url")
			new_url = add_url_prefix(url)
			# print('view object','raw url',url,'New URL',new_url)
			obj, created = Srturl.objects.get_or_create(url=new_url)
			#print(obj)
			context = {
				"object": obj, 
				"created": created,
			}
			if created:
				template = "shortener/success.html"
				bg_image = 'https://interfacelift.com/wallpaper/7yz4ma1/04110_cannonbeachsunset_1440x900.jpg'
				context['bg_image'] = bg_image
			else:
				template = "shortener/already-exist.html"
				bg_image = "https://interfacelift.com/wallpaper/7yz4ma1/04078_tothemountains_1440x900.jpg"
				context['bg_image'] = bg_image
		return render(request, template, context)

class URLRedirectView(View): #class based view
	def get(self, request, shortcode=None, *args, **kwargs):
		qs = Srturl.objects.filter(shortcode__iexact=shortcode)
		if qs.count() != 1 and not qs.exists():
			raise Http404
		obj = qs.first() 
		#obj = get_object_or_404(Srturl, shortcode=shortcode) #did not work properly
		ClickEvent.objects.create_event(obj)
		return HttpResponseRedirect(obj.url)

	def post(self, request, *args, **kwargs):
		return HttpResponse()







"""
# Create your views here.
def srturl_redirect_view(request, shortcode=None, *args, **kwargs):

	print('method is \n',request.method)
	#code below is useful for default behavior in web app/ do something else if shortcode is not found
	# try:
	# 	obj = Srturl.objects.get(shortcode=shortcode)
	# except:
	# 	obj = Srturl.objects.all().first()

	# obj_url = None
	# # qs = Srturl.objects.filter(shortcode__iexact=shortcode.upper())
	# # if qs.exists() and qs.count() == 1:
	# # 	obj = qs.first()
	# # 	obj_url = obj.url

	obj = get_object_or_404(Srturl, shortcode=shortcode)
	return HttpResponse("Hello {sc}".format(sc=obj.url))
"""