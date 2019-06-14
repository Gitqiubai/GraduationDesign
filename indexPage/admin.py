from django.contrib import admin

# Register your models here.
from .models import article,comment,Notices


admin.site.register(article)
admin.site.register(comment)
admin.site.register(Notices)