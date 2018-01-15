from .production import *
settings = "production"
try:
	from .local import *
	settings = "local"
except:
	pass

try:
	from .carlos_settings import *
	settings = "carlos_settings"
except:
	pass

print("Settings file used: -->",settings)