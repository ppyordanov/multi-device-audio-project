from django.contrib import admin
from mdrs.webapp.models import Event, User, Image, Recording

#add the default user form
admin.site.register(UserProfile)

#the rest of the models are below
admin.site.register(Event)
admin.site.register(User)
admin.site.register(Image)
admin.site.register(Recording)