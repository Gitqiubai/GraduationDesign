from django.contrib import admin

# Register your models here.
from .models import message_table


admin.site.register(message_table)
