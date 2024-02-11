from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html 

from .models import *
# Register your models here.
@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    list_display=['user','gender','type','mobile','image1']
    search_fields=['user']
    autocomplete_fields=['user']
    list_per_page= 2

    def image1(self,obj):
        return format_html('<img src="/media/{0}" width=auto height=80px style="border-radius:30px">'.format(obj.image.url))


@admin.register(Recruiter)
class RecruiterAdmin(admin.ModelAdmin):
    list_display=['user','gender','type','mobile','company','status','image1']    
    search_fields=['user']
    autocomplete_fields=['user']
    list_per_page= 5
    
    def image1(self,obj):
        return format_html('<img src="/media/{0}" width=auto height=100px style="border-radius:40px">'.format(obj.image.url))


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display=['recruiter','start_date','end_date','title','salary','description','experience','location','skills','creation_date','logo']


    def logo(self,obj):
        return format_html('<img src="/media/{0}" width=auto height=80px style="border-radius:30px">'.format(obj.image.url))
