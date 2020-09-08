from django.contrib import admin
from .models import RequestTypeMaster,StatusMaster,StateMaster,UserRequest

admin.site.register(RequestTypeMaster)
admin.site.register(StateMaster)
admin.site.register(StatusMaster)
admin.site.register(UserRequest)