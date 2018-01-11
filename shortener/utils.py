import random 
import string
from django.conf import settings
import re
# from shorterner.models import Srturl

SHORTCODE_MIN = getattr(settings, "SHORTCODE_MIN", 6) 

def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
	# new_code = ''
	# for _ in range(size):
	# 	new_code += random.choice(chars)
	# return new_code
	return ''.join(random.choice(chars) for _ in range(size))

def create_shortcode(instance, size=SHORTCODE_MIN):
	# this function return a shortcode which is unique to each Srturl instance
	new_code = code_generator(size)
	# print(instance)
	# print(instance.__class__)
	# print(instance.__class__.__name__)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(shortcode=new_code).exists()
	if (qs_exists):
		return create_shortcode(instance=instance, size=size)
	return new_code

def add_url_prefix(url):
	regex = re.compile(r"http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.")
	clean_url = url.lower()
	if url:
		if "http" in url and not "https" in url:
			replace_with = "http://www."
			url = re.sub(regex, replace_with, url)
		else:
			replace_with = "https://www."
			url = re.sub(regex, replace_with, url)
			if not "www" in url or not "http" in url:
				url = replace_with + url
	return url

# def add_url_prefix(url):
# 	if url:
# 		regex = re.compile(r"http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.")
# 		url = url.lower()
# 		clean_url =  regex.sub('www.', url).strip().strip('/')
# 		if "http" in url and not "https" in url:
# 			protocol = "http://"
# 			new_url = protocol + clean_url
# 		else:
# 			protocol = "https://"
# 			new_url = protocol + clean_url
# 		url = new_url
# 	return url


# from shortener.models import Srturl
# from shortener.utils import add_url_prefix
# url = 'https://www.aol.com'
# new_url = add_url_prefix(url)
# #obj, created = Srturl.objects.get_or_create(url=new_url)
# obj, created = Srturl.objects.get_or_create(url=url)
# print(obj)


# add_prefix_url('www.google.com/images')
# add_prefix_url('google.com/images')
# add_prefix_url('httP://google.com/images')
# add_prefix_url('httP://gooGle.cOm/images')
# add_prefix_url('httPs://gooGle.cOm/images')
# add_prefix_url('httPs://WwW.gooGle.cOm/images')
# add_prefix_url('httP://WwW.gooGle.cOm/images')
# add_prefix_url('WwW.gooGle.cOm/images')
# add_prefix_url('HtTp.gooGle.cOm/images')
# add_prefix_url('HtTp://gooGle.cOm/images')


# url = re.compile(r"http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/|www\.")
# >>> url.sub('', 'www.google.com/images').strip().strip('/')

"""
Markdown syntax example
```python
def create_shortcode(instance, size=6):
	new_code = code_generator(size)
	Klass = instance.__class__
	qs_exists = Klass.objects.filter(shortcode=new_code).exists()
	if (qs_exists):
		return **create_shortcode(size=size)
	return new_code
```
"""