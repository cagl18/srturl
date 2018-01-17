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
	lower_url = url.lower()
	if lower_url:
		if "http" in lower_url and "https" not in lower_url:
			replace_with = "http://www."
			lower_url = re.sub(regex, replace_with, lower_url)
		else:
			replace_with = "https://www."
			lower_url = re.sub(regex, replace_with, lower_url)
			if not "www" in lower_url or "http" not in lower_url:
				lower_url = replace_with + lower_url
	return lower_url

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

# add_url_prefix('www.google.com/images')
# add_url_prefix('google.com/images')
# add_url_prefix('httP://google.com/images')
# add_url_prefix('httP://gooGle.cOm/images')
# add_url_prefix('httPs://gooGle.cOm/images')
# add_url_prefix('httPs://WwW.gooGle.cOm/images')
# add_url_prefix('httP://WwW.gooGle.cOm/images')
# add_url_prefix('WwW.gooGle.cOm/images')
# add_url_prefix('HtTp.gooGle.cOm/images')
# add_url_prefix('HtTp://gooGle.cOm/images')


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