from django.contrib import admin
from django.contrib.auth.models import User
from models import *
# Register your models here.
class DateCenterAdmin(admin.ModelAdmin):
    list_display=('name','url')
class CloudUserAdmin(admin.ModelAdmin):
    list_display=('user','datecenter','api_key','secretkey')
class MachineAdmin(admin.ModelAdmin):
    list_display=('user','datecenter','hostname','cpus','status','machinename','machineid','templatename','ip')
class NetworkAdmin(admin.ModelAdmin):
    list_display=('datecenter','networkid','displaytext')
class ServiceOfferingsAdmin(admin.ModelAdmin):
    list_display=('datecenter','serviceofferingid','displaytext')
class TemplateAdmin(admin.ModelAdmin):
    list_display=('datecenter','templateid','displaytext','ostypename')
admin.site.register(DateCenter, DateCenterAdmin)
admin.site.register(CloudUser, CloudUserAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(ServiceOfferings,ServiceOfferingsAdmin)
admin.site.register(Network,NetworkAdmin)
admin.site.register(Template,TemplateAdmin)
