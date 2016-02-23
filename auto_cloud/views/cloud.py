#!/usr/bin/env python
#-*- coding: utf-8 -*-
#废弃
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from automation.common.CommonPaginator import SelfPaginator
from auto_auth.views.permission import PermissionVerify
import cloudstackapi
from auto_cloud import models
import traceback
# Create your views here.
# def signin(user):
	# try:
		#global api   #定义一个全局变量
		# user_in = models.CloudUser.objects.get(user__username=user.username)
		# api = cloudstackapi.CloudStackAPI("http://192.168.151.240:8080/client/api",user_in.api_key,user_in.secretkey)   
		# return 'ok'
	# except:
		# return 'err'
def signin1(user,name):
	try:
		# global api   #定义一个全局变量
		user_in = models.CloudUser.objects.get(Q(user__username=user.username),Q(datecenter__name=name))
		# print user_in.datecenter
		# print uer_in.datecenter
		if user_in and user_in.api_key and user_in.secretkey:
			url = user_in.datecenter.url
			api_key = user_in.api_key
			secretkey = user_in.secretkey
			# print url
			# print user_in.api_key
			# print user_in.secretkey
			api = cloudstackapi.CloudStackAPI(url.encode('utf-8'),api_key.encode('utf-8'),secretkey.encode('utf-8'))
			# print api
			if api:
				return api
			else:
				print api
	except:
		print traceback.format_exc()
@login_required
@PermissionVerify()	
def Listcloud(request):
	user = request.user
	centers = models.DateCenter.objects.all()
	# print centers
	results = []
	err = ''
	try:
		for center in centers:
			kapi = ''
			result = ''
			try:
				# print '@@@@@@@@@@@@@',center
				kapi = signin1(user,center.name)
				# print '#############'
				if kapi:
					req = {'install':'True'}
					result = kapi.listVirtualMachines(req)
					# print '%%%%%%%%%'
					if result:
						for item in result['virtualmachine']:
							item['center'] = center.name
						results = results + result['virtualmachine']
					# print results
					# print center.name

				else:
					namec = center.name
					err += '在机房%s没有权限，请联系管理员\n' % namec.encode('utf-8')
					continue
				
			except:
				namec = center.name
				# err += '在机房%s没有权限，请联系管理员\n' % namec.encode('utf-8')
				# print e
				print traceback.format_exc()

		# kwvars = {'user':user,'results':results,'request':request,}
			# return render_to_response('auto_cloud/listcloud1.html',kwvars,RequestContext(request))
		return render_to_response('auto_cloud/listcloud1.html',{'user':user,'results':results,'err':err})
	except:
		# print e
		print traceback.format_exc()
		# kwvars = {'user':user,'err':'您没有云平台使用权限，请联系管理员!','request':request,}
		# return render_to_response('auto_cloud/listcloud1.html',kwvars,RequestContext(request))
		return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'您没有云平台使用权限，请联系管理员!'})
@login_required
@PermissionVerify()
def Addcloud(request):
	user = request.user	
	centers = models.DateCenter.objects.all()
	api = ''
	try:
		if request.method == 'POST' and request.POST.get('name') and request.POST.get('os') and request.POST.get('center'):
			print request.POST.get('center').encode("utf-8")
			api = signin1(user,request.POST.get('center').encode("utf-8"))
			# print request.POST.get('os').encode("utf-8")
			data = {
			'serviceofferingid':'2bfa8165-3a24-464e-ae64-2ffe87dabe57',
			'templateid':request.POST.get('os').encode("utf-8"),
			'zoneid':'e10b562a-4b52-4883-8e47-affcd48f5d5c',
			'networkids': 'da76db39-45c3-4f55-9fff-a1edb1a16123',
			'name':request.POST.get('name').encode("utf-8")
			}
			# print request.POST.get('os').encode("utf-8")
			response_err = api.deployVirtualMachine(data)
			if response_err:
				# print response_err
				return HttpResponseRedirect(reverse('listcloudurl'))
			else:
				return render_to_response('auto_cloud/addcloud1.html',{'user':user,'err':'操作失败!'})
		else:
			if signin(user):
				request = {'templatefilter':'all'}
				result = api.listTemplates(request)
			return render_to_response('auto_cloud/addcloud1.html',{'user':user,'centers':centers,'templates':result['template']})
	except:
		return render_to_response('auto_cloud/addcloud1.html',{'user':user,'err':'操作失败!'})

def Start(request,id):
	user = request.user
	try:
		if signin(user) == 'ok':
			request = {"id":id}
			result = api.startVirtualMachine(request)
			print result
			if request:
				return HttpResponseRedirect(reverse('listcloudurl'))
			else:
				return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'操作失败!'})
def Stop(request,id):
	user = request.user
	try:
		if signin(user) == 'ok':
			request = {"id":id}
			result = api.stopVirtualMachine(request)
			print result
			if request:
				return HttpResponseRedirect(reverse('listcloudurl'))
			else:
				return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'操作失败!'})
def Restart(request,id):
	user = request.user
	try:
		if signin(user) == 'ok':
			request = {"id":id}
			result = api.rebootVirtualMachine(request)
			print result
			if request:
				return HttpResponseRedirect(reverse('listcloudurl'))
			else:
				return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud1.html',{'user':user,'err':'操作失败!'})