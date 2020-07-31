from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from .models import *


class UniversityAdmin(ModelAdmin):
	list_display = ['name','country','domain','alpha_two_code','web_page']
	search_field = ['name','template_type','created_by']


admin.site.register(University,UniversityAdmin)
