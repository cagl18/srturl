from django import forms

from .validators import validate_url, validate_dot_com

class SubmitUrlForm(forms.Form):
	url = forms.CharField(
			label = '', 
			validators=[validate_url],
			widget = forms.TextInput(
					attrs = {
						"placeholder": "Long URL",
						"class": "form-control",
					}
				)
			)

	# def clean(self): # validating for overall form 
	# 	cleaned_data = super(SubmitUrlForm, self).clean()
	# 	url = cleaned_data.get("url")
	# 	#print(url)

	# def clean_url(self): #validating the url field (each field needs an individual func)
	# 	url = self.cleaned_data['url']
	# 	if "http://" in url:
	# 		return url
	# 	return "http://" + url