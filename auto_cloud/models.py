# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User

class DateCenter(models.Model):
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=255)
	def __unicode__(self):
		return '%s(%s)' %(self.name,self.url)    
	class Meta:
		unique_together = ("name",)
		verbose_name = '机房'
		verbose_name_plural = "机房"
class CloudUser(models.Model):
	user = models.ForeignKey(User)
	datecenter = models.ForeignKey(DateCenter)
	api_key = models.CharField(max_length=200,blank=True)
	secretkey = models.CharField(max_length=200,blank=True)
	class Meta:
		verbose_name = '用户表'
		verbose_name_plural = "用户表"
	def __unicode__(self):
		return self.user.username
		
class Machine(models.Model):
	user = models.ForeignKey(User)
	datecenter = models.ForeignKey(DateCenter)
	hostname = models.CharField(max_length=100,blank=True)
	cpus = models.CharField(max_length=10,blank=True)
	maxmem = models.CharField(max_length=10,blank=True)
	status = models.CharField(max_length=10,blank=True)
	machinename = models.CharField(max_length=100,blank=True)
	machineid = models.CharField(max_length=200,blank=True)
	templatename = models.CharField(max_length=100,blank=True)
	ip = models.CharField(max_length=200,blank=True)
	class Meta:
		verbose_name = '机器表'
		verbose_name_plural = "机器表"
	def __unicode__(self):
		return '%s-%s' % (self.user.username,self.hostname)
class ServiceOfferings(models.Model):
	datecenter = models.ForeignKey(DateCenter)
	serviceofferingid = models.CharField(max_length=100,blank=True)
	displaytext = models.CharField(max_length=200,blank=True)
	class Meta:
		verbose_name = '硬件配置模板'
		verbose_name_plural = "硬件配置模板"
	def __unicode__(self):
		return '%s-%s' % (self.datecenter.name,self.displaytext)
class Network(models.Model):
	datecenter = models.ForeignKey(DateCenter)
	networkid = models.CharField(max_length=100,blank=True)
	displaytext = models.CharField(max_length=200,blank=True)
	class Meta:
		verbose_name = '网络ID'
		verbose_name_plural = "网络ID"
	def __unicode__(self):
		return '%s-%s' % (self.datecenter.name,self.displaytext)
class Template(models.Model):
	datecenter = models.ForeignKey(DateCenter)
	templateid = models.CharField(max_length=100,blank=True)
	displaytext = models.CharField(max_length=200,blank=True)
	ostypename = models.CharField(max_length=100,blank=True)
	class Meta:
		verbose_name = '系统模板表'
		verbose_name_plural = "系统模板表"
	def __unicode__(self):
		return '%s:%s' % (self.centername,slef.ostypename)