#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.contrib.auth.decorators import login_required
from automation.common.CommonPaginator import SelfPaginator
from auto_auth.views.permission import PermissionVerify
import types 
import cloudstackapi #cloudstack api封装
from auto_cloud import models
import traceback
#cloudstack api登陆
def signin(user,name):
	try:
		# global api   #定义一个全局变量
		try:
			user_in = models.CloudUser.objects.get(Q(user__username=user.username),Q(datecenter__name=name))
		except:
			return 'err'
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
				return 'err'
		else:
			return 'err'
	except:
		print traceback.format_exc()
		return 'err'
#cloudstack api获取创建组权限信息用于创建组
def Signin(user,name):
	try:
		# global api   #定义一个全局变量
		try:
			user_in = models.CloudUser.objects.get(Q(user__username=user.username),Q(datecenter__name=name))
		except:
			return 'err'
		# print user_in.datecenter
		# print uer_in.datecenter
		if user_in and user_in.api_key and user_in.secretkey:
			url = user_in.datecenter.url
			api_key = user_in.api_key
			secretkey = user_in.secretkey
			# print url
			# print user_in.api_key
			# print user_in.secretkey
			api = cloudstackapi.Client(url.encode('utf-8'),api_key.encode('utf-8'),secretkey.encode('utf-8'))
			# print api
			if api:
				return api
			else:
				return 'err'
		else:
			return 'err'
	except:
		print traceback.format_exc()
		return 'err'
@login_required
@PermissionVerify()
#列出虚拟机
def Listcloud(request):
	user = request.user
	if user.is_superuser:
		machines = models.Machine.objects.all()
	else:
		machines = models.Machine.objects.filter(user=user)
	err = ''
	if machines:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'machines':machines,'err':err})
	else:
		err = '没有机器或者没有权限！'
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':err})
#刷新函数，贡创建虚拟机后刷新
def serverrefresh(user,centername):
	machines = models.Machine.objects.filter(user=user,datecenter__name = centername)
	results = []
	try:
		api = ''
		try:
			# print '@@@@@@@@@@@@@',center
			api = signin(user,centername)
			# print '#############'
			if api:
				req = {'install':'True'}
				result = api.listVirtualMachines(req)
				# print '%%%%%%%%%'
				if result:
					for item in result['virtualmachine']:
						item['center'] = centername
					results = results + result['virtualmachine']
		except:
			print traceback.format_exc()
	except:
		print traceback.format_exc()
	try:
		for item in machines:
			tag = 0
			for res in results:
				if item.machineid == res['id'] and item.status != res['state']:
					item.status = res['state']
					item.save()
					continue
				elif item.machineid == res['id'] and item.status == res['state']:
					continue
				else:
					tag +=1
			if tag == len(results):
				models.Machine.objects.filter(machineid = item.machineid).delete()
		for res in results:
			tg = 0 
			for item in machines:
				if item.machineid == res['id']:
					continue
				else:
					tg += 1
			if tg == len(machines):
				# print res['center']
				# print "######################"
				models.Machine.objects.create(user=user,datecenter=models.DateCenter.objects.get(name=res['center']),cpus=res['cpunumber'],maxmem=res['memory'],status=res['state'],machinename=res['name'],machineid=res['id'],templatename=res['templatename'],ip=res['nic'][0]['ipaddress'])
		return 'ok'
	except:
		print traceback.format_exc()
		return 'err'	
#手动刷新函数
def refresh(request):
	user = request.user
	machines = models.Machine.objects.filter(user=user)
	centers = models.DateCenter.objects.all()
	results = []
	try:
		for center in centers:
			api = ''
			result = ''
			try:
				# print '@@@@@@@@@@@@@',center
				api = signin(user,center.name)
				# print '#############'
				if api:
					req = {'install':'True'}
					result = api.listVirtualMachines(req)
					# print '%%%%%%%%%'
					if result:
						for item in result['virtualmachine']:
							item['center'] = center.name
						results = results + result['virtualmachine']
			except:
				print traceback.format_exc()
	except:
		print traceback.format_exc()
	try:
		for item in machines:
			tag = 0
			for res in results:
				if item.machineid == res['id'] and item.status != res['state']:
					item.status = res['state']
					item.save()
					continue
				elif item.machineid == res['id'] and item.status == res['state']:
					continue
				elif item.machineid != res['id']:
					tag +=1
			if tag == len(results):
				models.Machine.objects.filter(machineid = item.machineid).delete()
		for res in results:
			tg = 0 
			for item in machines:
				if item.machineid == res['id']:
					continue
				elif item.machineid != res['id']:
					tg += 1
			if tg == len(machines):
				# print res['center']
				# print "######################"
				models.Machine.objects.create(user=user,datecenter=models.DateCenter.objects.get(name=res['center']),cpus=res['cpunumber'],maxmem=res['memory'],status=res['state'],machinename=res['name'],machineid=res['id'],templatename=res['templatename'],ip=res['nic'][0]['ipaddress'])
		return HttpResponseRedirect(reverse('listcloudurl'))
	except:
		print traceback.format_exc()
		return HttpResponse('error')
#模板刷新
def TemRes(request):
	user = request.user
	centers = models.DateCenter.objects.all()
	# print centers
	templates = models.Template.objects.all()
	results = ''
	try:
		for center in centers:
			kapi = ''
			try:
				# print '@@@@@@@@@@@@@',center
				try:
					kapi = signin(user,center.name)
					# print type(kapi)
					if type(kapi) is types.StringType:
						continue
				except:
					continue
				if kapi:
					req = {'templatefilter':'featured'}
					# print center.name
					result = kapi.listTemplates(req)
					# print '%%%%%%%%%'
					if result:
						templates = models.Template.objects.filter(datecenter__name=center.name)
						for item in templates:
							tag = 0
							for res in result['template']:
								if item.templateid == res['id']:
									continue
								else:
									tag +=1
							if tag == len(result['template']):
								models.Template.objects.filter(templateid = item.templateid).delete()
						for res in result['template']:
							tg = 0
							for item in templates:
								if item.templateid == res['id']:
									continue
								else:
									tg += 1
							if tg == len(templates):
								models.Template.objects.create(datecenter=models.DateCenter.objects.get(name=center.name),templateid=res['id'],displaytext=res['displaytext'],ostypename=res['ostypename'])
				else:
					continue
			except:
				print traceback.format_exc()
				return HttpResponse('error')
		return HttpResponseRedirect(reverse('listcloudurl'))
	except:
		print traceback.format_exc()
		return HttpResponse('error')
@login_required
@PermissionVerify()
#添加组
def Addgroup(request,center):
	user = request.user
	try:
		centername = ''
		postUrl = '/autoCloud/cloud/%s/addgroup/' % center
		RedirectUrl = '/autoCloud/cloud/%s/add/' % center
		print postUrl
		print RedirectUrl
		if request.method == 'POST' and request.POST.get('name') and request.POST.get('type'):
			name = request.POST.get('name').encode("utf-8")
			type = request.POST.get('type').encode("utf-8")
			discibe = request.POST.get('discibe').encode("utf-8")
			if discibe:
				data = {
				'name':name,
				'type':type,
				'discibe': discibe
				}
			else:
				data = {
				'name':name,
				'type':type
				}
			if center == 'SYQ':
				centername = '三元桥'
				api = Signin(user,centername)
				
				response_err = api.createAffinityGroup(data)
				if response_err:
					print response_err
					return HttpResponseRedirect(RedirectUrl)
				else:
					return render_to_response('auto_cloud/addgroup.html',{'user':user,'err':'操作失败!'})
			elif center == 'TN':
				centername = '铜牛'
				api = Signin(user,centername)
				response_err = api.createAffinityGroup(data)
				if response_err:
					# print response_err
					return HttpResponseRedirect(RedirectUrl)
				else:
					return render_to_response('auto_cloud/addgroup.html',{'user':user,'err':'操作失败!'})
			elif center == 'HCY':
				centername = '慧聪园'
				api = Signin(user,centername)
				response_err = api.createAffinityGroup(data)
				if response_err:
					# print response_err
					return HttpResponseRedirect(RedirectUrl)
				else:
					return render_to_response('auto_cloud/addgroup.html',{'user':user,'err':'操作失败!'})
		else:
			if center == 'SYQ':
				centername = '三元桥'
				api = signin(user,centername)
				if api!= 'err':
					request = {'listall':'all'}
					print "#############"
					response_err = api.listAffinityGroupTypes(request)
					# print response_err
					if response_err['affinityGroupType']:
						types = response_err['affinityGroupType']
					else:
						types = {}
				else:
					types = {}
				return render_to_response('auto_cloud/addgroup.html',{'user':user,'types':types,'postUrl':postUrl})
			elif center == 'TN':
				centername = '铜牛'
				api = signin(user,centername)
				request = {'listall':'all'}
				response_err = api.listAffinityGroupTypes(request)
				if response_err['affinityGroupType']:
					types = response_err['affinityGroupType']
				else:
					types = {}
				return render_to_response('auto_cloud/addgroup.html',{'user':user,'types':types,'postUrl':postUrl})
			elif center == 'HCY':
				centername = '慧聪园'
				api = signin(user,centername)
				request = {'listall':'all'}
				response_err = api.listAffinityGroupTypes(request)
				if response_err['affinityGroupType']:
					types = response_err['affinityGroupType']
				else:
					types = {}
				return render_to_response('auto_cloud/addgroup.html',{'user':user,'types':types,'postUrl':postUrl})
	except:
		return render_to_response('auto_cloud/adderr.html',{'user':user,'err':'操作失败!'})
		
		
		
@login_required
@PermissionVerify()
#添加虚拟机
def Addcloud(request,center):
	user = request.user
	try:
		centername = ''
		if request.method == 'POST' and request.POST.get('name') and request.POST.get('templates') and request.POST.get('serviceofferings') and request.POST.get('networks'):
			name = request.POST.get('name').encode("utf-8")
			templates = request.POST.get('templates').encode("utf-8")
			serviceofferings = request.POST.get('serviceofferings').encode("utf-8")
			networks = request.POST.get('networks').encode("utf-8")
			if request.POST.get('type'):
				typeid = request.POST.get('type').encode("utf-8")
				
			else:
				typeid=''
			# print typeid
			# print name
			# print templates
			# print serviceofferings
			# print networks
			if center == 'SYQ':
				centername = '三元桥'
				api = signin(user,centername)
				data = {
				'serviceofferingid':serviceofferings,
				'templateid':templates,
				'zoneid':'e1e57f82-41e9-4372-a7ad-da9ba45b4dc7',
				'networkids': networks,
				'name':name,
				'affinitygroupids':typeid
				}
				# print request.POST.get('os').encode("utf-8")
				response_err = api.deployVirtualMachine(data)
				temref = serverrefresh(user,centername)
				# print temref
				if response_err and temref == 'ok':
					# print response_err
					return HttpResponseRedirect(reverse('listcloudurl'))
				else:
					return render_to_response('auto_cloud/adderr.html',{'user':user,'err':'操作失败!'})
			elif center == 'TN':
				centername = '铜牛'
				api = signin(user,centername)
				# print request.POST.get('os').encode("utf-8")
				data = {
				'serviceofferingid':serviceofferings,
				'templateid':templates,
				'zoneid':'e1a50d71-291e-495b-81fe-2be66f20e9b8',
				'networkids': networks,
				'name':name,
				'affinitygroupids':typeid
				}
				# print request.POST.get('os').encode("utf-8")
				response_err = api.deployVirtualMachine(data)
				temref = serverrefresh(user,centername)
				if response_err and temref == 'ok':
					# print response_err
					return HttpResponseRedirect(reverse('listcloudurl'))
				else:
					return render_to_response('auto_cloud/adderr.html',{'user':user,'err':'操作失败!'})
			elif center == 'HCY':
				centername = '慧聪园'
				api = signin(user,centername)
				# print request.POST.get('os').encode("utf-8")
				data = {
				'serviceofferingid':serviceofferings,
				'templateid':templates,
				'zoneid':'e10b562a-4b52-4883-8e47-affcd48f5d5c',
				'networkids': networks,
				'name':name,
				'affinitygroupids':typeid
				}
				# print request.POST.get('os').encode("utf-8")
				response_err = api.deployVirtualMachine(data)
				temref = serverrefresh(user,centername)
				if response_err and temref == 'ok':
					# print response_err
					return HttpResponseRedirect(reverse('listcloudurl'))
				else:
					return render_to_response('auto_cloud/adderr.html',{'user':user,'err':'操作失败!'})
		else:
			postUrl = '/autoCloud/cloud/%s/add/' % center
			request = {'listall':'true'}
			types = [{'name':u'空组'}]
			if center == 'SYQ':
				centername = '三元桥'
				api = signin(user,centername)
				if api != 'err':
					result = api.listAffinityGroups(request)
					if 'affinitygroup' in result.keys():
						if result['affinitygroup']:
							types += result['affinitygroup']
							# print types
				templates = models.Template.objects.filter(datecenter__name='三元桥')
				serviceofferings = models.ServiceOfferings.objects.filter(datecenter__name='三元桥')
				networks = models.Network.objects.filter(datecenter__name='三元桥')
				# print templates
				# print serviceofferings
				# print networks
				return render_to_response('auto_cloud/addMachine.html',{'user':user,'templates':templates,'serviceofferings':serviceofferings,'networks':networks,'types':types,'postUrl':postUrl})
			elif center == 'TN':
				centername = '铜牛'
				api = signin(user,centername)
				if api != 'err':
					result = api.listAffinityGroups(request)
					if 'affinitygroup' in result.keys():
						if result['affinitygroup']:
							types += result['affinitygroup']
				templates = models.Template.objects.filter(datecenter__name='铜牛')
				serviceofferings = models.ServiceOfferings.objects.filter(datecenter__name='铜牛')
				networks = models.Network.objects.filter(datecenter__name='铜牛')
				# print templates
				# print serviceofferings
				# print networks
				return render_to_response('auto_cloud/addMachine.html',{'user':user,'templates':templates,'serviceofferings':serviceofferings,'networks':networks,'types':types,'postUrl':postUrl})
			elif center == 'HCY':
				centername = '慧聪园'
				api = signin(user,centername)
				if api != 'err':
					result = api.listAffinityGroups(request)
					if 'affinitygroup' in result.keys():
						if result['affinitygroup']:
							types += result['affinitygroup']
				templates = models.Template.objects.filter(datecenter__name='慧聪园')
				serviceofferings = models.ServiceOfferings.objects.filter(datecenter__name='慧聪园')
				networks = models.Network.objects.filter(datecenter__name='慧聪园')
				# print templates
				# print serviceofferings
				# print networks
				return render_to_response('auto_cloud/addMachine.html',{'user':user,'templates':templates,'serviceofferings':serviceofferings,'networks':networks,'types':types,'postUrl':postUrl})
	except:
		return render_to_response('auto_cloud/adderr.html',{'user':user,'err':'操作失败,请联系管理员!'})
@login_required
@PermissionVerify()
#开启虚拟机
def Start(request,id):
	user = request.user
	machine = models.Machine.objects.get(id=int(id))
	try:
		api = signin(user,machine.datecenter.name)
		request = {"id":machine.machineid}
		result = api.startVirtualMachine(request)
		# print result
		if request:
			return HttpResponseRedirect(reverse('listcloudurl'))
		else:
			return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
@login_required
@PermissionVerify()
#停止虚拟机
def Stop(request,id):
	user = request.user
	# print user,id
	machine = models.Machine.objects.get(id=int(id))
	# print machine.machineid
	# print machine.datecenter.name
	try:
		# print '###################'
		api = signin(user,machine.datecenter.name)
		# print '@@@@@@@@@@@@@@@@@@@@@@'
		request = {"id":machine.machineid}
		result = api.stopVirtualMachine(request)
		print result
		if request:
			return HttpResponseRedirect(reverse('listcloudurl'))
		else:
			return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
@login_required
@PermissionVerify()
##重启虚拟机
def Restart(request,id):
	user = request.user
	machine = models.Machine.objects.get(id=int(id))
	try:
		api = signin(user,machine.datecenter.name)
		request = {"id":machine.machineid}
		result = api.rebootVirtualMachine(request)
		# print result
		if request:
			return HttpResponseRedirect(reverse('listcloudurl'))
		else:
			return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
@login_required
@PermissionVerify()
#删除虚拟机
def Delete(request,id):
	user = request.user
	machine = models.Machine.objects.get(id=int(id))
	# print user
	# print machine.datecenter.name
	try:
		# print '@@@@@@@@@@@@@@@@@'
		api = signin(user,machine.datecenter.name)
		# print api
		# print '####################'
		request = {"id":machine.machineid}
		result = api.destroyVirtualMachine(request)
		# print result
		ref = serverrefresh(user,machine.datecenter.name)
		# print ref
		if request and ref == 'ok':
			return HttpResponseRedirect(reverse('listcloudurl'))
		else:
			return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})
	except:
		return render_to_response('auto_cloud/listcloud.html',{'user':user,'err':'操作失败!'})