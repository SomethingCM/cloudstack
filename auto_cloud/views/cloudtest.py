#!/usr/bin/env python
#-*- coding: utf-8 -*-
#废弃

from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from automation.common.CommonPaginator import SelfPaginator
from auto_auth.views.permission import PermissionVerify
import cloudstackapi
from auto_auth import models
# Create your views here.
def signin(user):
	try:
		global api   #定义一个全局变量
		user_in = models.AuthUser.objects.get(user__username=user.username)
		api = cloudstackapi.CloudStackAPI("http://172.16.105.230:8080/client/api",user_in.api_key,user_in.secretkey) 
		request = {'install':'True'}
		result = api.listVirtualMachines(request)
		print result['virtualmachine']
		return 'ok'
	except:
		return 'err'
@login_required
@PermissionVerify()
def Addcloud(request):
	user = request.user	
	try:
		if request.method == 'POST' and signin(user) == 'ok' and request.POST.get('name') and request.POST.get('os'):
			print request.POST.get('os').encode("utf-8")
			data = {
			'serviceofferingid':'2bfa8165-3a24-464e-ae64-2ffe87dabe57',
			'templateid':request.POST.get('os').encode("utf-8"),
			'zoneid':'e10b562a-4b52-4883-8e47-affcd48f5d5c',
			'networkids': 'da76db39-45c3-4f55-9fff-a1edb1a16123',
			'name':request.POST.get('name').encode("utf-8")
			}
			print request.POST.get('os').encode("utf-8")
			response_err = api.deployVirtualMachine(data)
			if response_err:
				print response_err
				return HttpResponseRedirect(reverse('listcloudurl'))
			else:
				return render_to_response('auto_cloud/addcloud.html',{'user':user,'err':'操作失败!'})
		else:
			if signin(user) == 'ok':
				request = {'templatefilter':'all'}
				result = api.listTemplates(request)
			return render_to_response('auto_cloud/addcloud.html',{'user':user,'templates':result['template']})
	except:
		return render_to_response('auto_cloud/addcloud.html',{'user':user,'err':'操作失败!'})
@login_required
@PermissionVerify()	
def Listcloud(request):
	user = request.user
	try:
		if signin(user) == 'ok':
			request = {'install':'True'}
			result = api.listVirtualMachines(request)
			print result['virtualmachine'][0]['id']
			kwvars = {'user':user,'results':result['virtualmachine'],'request':request,}
			# return render_to_response('auto_cloud/listcloud.html',kwvars,RequestContext(request))
			return render_to_response('auto_cloud/listcloud.html',{'user':user,'results':result['virtualmachine']})
		else:
			kwvars = {'user':user,'err':'您没有云平台使用权限，请联系管理员!','request':request,}
			# return render_to_response('auto_cloud/listcloud.html',kwvars,RequestContext(request))
			return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'您没有云平台使用权限，请联系管理员!'})
	except:
		kwvars = {'user':user,'err':'您没有云平台使用权限，请联系管理员!','request':request,}
		# return render_to_response('auto_cloud/listcloud.html',kwvars,RequestContext(request))
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'您没有云平台使用权限，请联系管理员!'})
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
				return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
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
				return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
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
				return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
		
		
		
def test():
	try:
		global api   #定义一个全局变量
		api_key = 'zWwNIDGCAYkJLpeO_XIPPP7bBbInZz9uhdTNYc0s9pLQLmy4qD41mr7mhEa6BzF-DuYwDHwARfoAfkHZNHsvDA'
		secretkey = '1JekGnijShz8cFO7IsZHg0JrABRlXpoG4XvNzhb9GX-E4unGgXFc7OEamifRf_lXj-GiEaEHFWjBAmiU6p81XA'
		api = cloudstackapi.CloudStackAPI("http://172.16.105.230:8080/client/api",api_key,secretkey) 
		request = {'install':'True'}
		result = api.listVirtualMachines(request)
		print result['virtualmachine']
		return 'ok'
	except:
		return 'err'
if __name__=='__main__':
	test()