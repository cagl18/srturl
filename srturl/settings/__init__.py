from .production import *

try:
	from .local import *
except:
	pass

try:
	from .carlos_settings import *
except:
	pass