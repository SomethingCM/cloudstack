#!/usr/bin/env python
#-*- coding: utf-8 -*-
import cloudstackapi
def test():
	try:
		# global api   #定义一个全局变量
		api_key = 'zWwNIDGCAYkJLpeO_XIPPP7bBbInZz9uhdTNYc0s9pLQLmy4qD41mr7mhEa6BzF-DuYwDHwARfoAfkHZNHsvDA'
		secretkey = '1JekGnijShz8cFO7IsZHg0JrABRlXpoG4XvNzhb9GX-E4unGgXFc7OEamifRf_lXj-GiEaEHFWjBAmiU6p81XA'
		api = cloudstackapi.CloudStackAPI("http://172.16.105.230:8080/client/api",api_key,secretkey) 
		request = {'install':'True'}
		result = api.listVirtualMachines(request)
		print result['virtualmachine']
		
	except Exception,e:
		print e
if __name__=='__main__':
	test()