from django.contrib import admin
from users.models import CustomUser, Balance

admin.site.register(CustomUser)
admin.site.register(Balance)
