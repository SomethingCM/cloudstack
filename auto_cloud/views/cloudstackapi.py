#coding=utf-8
import hashlib, hmac , string , base64, urllib, urllib2,json,re
from db_connector import *
# from auto_auth import models
#cloudstack 类封装1
class CloudStackAPI(object):
    """ """
    def __init__(self, api_url,api_key,secret):
        self.api_url = api_url
        self.api_key = api_key
        self.secret = secret
    def __getattr__(self,name):
        def handlerfun(*args,**kwargs):
            if kwargs:
                return self._make_request(name,kwargs)
            return self._make_request(name,args[0])
        return handlerfun
    def _make_request(self,name,args):
        args['response'] = 'json'
        args['command'] = name
        args['apiKey'] = self.api_key
        self._request(args)
        key = name.lower() + 'response'
        return json.loads(self.response.read())[key]
    def _request(self,args):
        ''' create value'''
        self.params = []
        self._sort_reques(args)
        self._create_signature()
        self._build_post_request()
        self._http_get()
    def _sort_reques(self,args):
        keys = sorted(args.keys())
        for key in keys:
            self.params.append(key+'='+urllib.quote_plus(args[key]))
    def _create_signature(self):
        self.query = '&'.join(self.params)
        digest = hmac.new(self.secret,msg=self.query.lower(),digestmod=hashlib.sha1).digest()
        self.signature = base64.b64encode(digest)
    def _build_post_request(self):
        self.query = self.query +'&signature='+urllib.quote_plus(self.signature)
        self.value = self.api_url+'?'+self.query
    def _http_get(self):
        self.response = urllib.urlopen(self.value)

######################################################################################
#cloudstack 类封装2
class BaseClient(object):
    def __init__(self, api, apikey, secret):
        self.api = api
        self.apikey = apikey
        self.secret = secret

    def request(self, command, args):
        args['apikey'] = self.apikey
        args['command'] = command
        args['response'] = 'json'

        params = []

        keys = sorted(args.keys())

        for k in keys:
            params.append(k + '=' + urllib.quote(args[k], safe='/'))
        # print params
        query = '&'.join(params)
        # print query.lower()
        signature = base64.b64encode(hmac.new(
            self.secret, 
            msg=query.lower(), 
            digestmod=hashlib.sha1
        ).digest())

        query += '&signature=' + urllib.quote(signature, safe='/')
        # print query
        response = urllib2.urlopen(self.api + '?' + query)
        decoded = json.loads(response.read())
       
        propertyResponse = command.lower() + 'response'
        if not propertyResponse in decoded:
            if 'errorresponse' in decoded:
                raise RuntimeError("ERROR: " + decoded['errorresponse']['errortext'])
            else:
                raise RuntimeError("ERROR: Unable to parse the response")

        response = decoded[propertyResponse]
        result = re.compile(r"^list(\w+)s").match(command.lower())

        if not result is None:
            type = result.group(1)

            if type in response:
                return response[type]
            else:
                # sometimes, the 's' is kept, as in :
                # { "listasyncjobsresponse" : { "asyncjobs" : [ ... ] } }
                type += 's'
                if type in response:
                    return response[type]

        return response
class Client(BaseClient):
    def createAffinityGroup(self, args={}):
        if not 'name' in args:
            raise RuntimeError("Missing required argument 'name'")
        if not 'type' in args:
            raise RuntimeError("Missing required argument 'type'")
        return self.request('createAffinityGroup', args)
######################################################################################


def list():
	# #user_in = models.AuthUser.objects.get(user__username='admin')
	##慧聪
	# api = CloudStackAPI("http://192.168.151.240:8080/client/api",'B6ifdpa1aT0l-nZs0o2IyYQk5cOtmlKItjRiQ8AsLGzTI5f2GjKuOjvnqqRCArS4FcN2hlOuAc5ybkTO0Yu2Ng','qTP4xGMtJPh7ZpdGnNdJABFZ-uN2eMJ3ukpMiDEEG80w9-4onDVdEdbYx9ZupGiMlrO4mz0ql8cJw-XYL1shhA')
	##铜牛
	# api = CloudStackAPI("http://192.168.161.220:8080/client/api",'3lzfv5SB2S2m5CrZ623au6TX-yzRUaWgpHGcbsU_n3j9FXm1vzxPUX5Tb35DNXmZAc_zZTP87g_VNgA_6juQAQ','s-kX6LjnDFTZaqFgZQi6nSg1xKA_DhxLjuI_wkSYBMX3F2diyX9npI_cVV25CVfXPSnnfOkUEmN6tdR8RtWe8w')
	##三元桥
	# api = CloudStackAPI("http://172.16.105.230:8080/client/api",'zWwNIDGCAYkJLpeO_XIPPP7bBbInZz9uhdTNYc0s9pLQLmy4qD41mr7mhEa6BzF-DuYwDHwARfoAfkHZNHsvDA','1JekGnijShz8cFO7IsZHg0JrABRlXpoG4XvNzhb9GX-E4unGgXFc7OEamifRf_lXj-GiEaEHFWjBAmiU6p81XA')
	## api = CloudStackAPI("http://192.168.151.240:8080/client/api",'C6kZ4Fqd5EFwCd8ZEaXqqWwm2KadmEfDjfNN6xe-d5-DgFG9tzpxRBI_7cEgTNzY59bPcrOyH1Ws3IbhQTi-0w','TFU5_bG1y311wueMnyMBxoxPCNZBPBvp_AcRRL93qV5KpszRNPTValpTFVpxJQfmsIA9hzw5_53u9EPZK3JrNw')
	##三元桥
	# api = CloudStackAPI("http://172.16.105.230:8080/client/api",'6d9GbE1DRhr22F3NEAehr-XQPmm37LvJ2gPP1x9yEDc9MRXSjyzJXkm2EjMlPvuS1I_0IO2tc6_cv_UHo9XmtA','7szhaIfRrJY5Rakop7CG1O2uzZzXOtFf0lUMhGOVjSo38bnywSKkmo1_-pfSxy0iTkzjle1KjWjwfTlF1pwitA')
	#cm
	api = CloudStackAPI("http://172.16.105.230:8080/client/api",'caUK12pJQ6tNQdpdLwBSAPS5XEpQAWpF0k6ugwiAFrqD_5meBugJoveKcLrBUiLVtHI_dpTX8JezFi5J6jYqsg','23_Kbf2o-_FC5T_3KuzP6qcE1tH56YJieEx4N1gXYE-LzQPXCdVf4_CJnQwnwIH85U4pytSCL2EdDed27_Wx3w')
	# api2 = Client("http://172.16.105.230:8080/client/api",'caUK12pJQ6tNQdpdLwBSAPS5XEpQAWpF0k6ugwiAFrqD_5meBugJoveKcLrBUiLVtHI_dpTX8JezFi5J6jYqsg','23_Kbf2o-_FC5T_3KuzP6qcE1tH56YJieEx4N1gXYE-LzQPXCdVf4_CJnQwnwIH85U4pytSCL2EdDed27_Wx3w')
	# print api2
	# request = {'templatefilter':'all'}
	# request = {'details':'all'}
	request = {'listall':'true'}
	# result = api.listVirtualMachines(request)
	# 
	# request = {'name':'chenmeng01','type':'host anti-affinity','domainid':'3e1f8b50-64c3-11e3-9dff-b7c5b64123ec','description':'','account':'chenmeng'}
	
	# request = {'name':'chenmeng01','type':"host anti-affinity"}
	# request = {'keyword':'name'}
	result = api.listAffinityGroups(request)
	# result = api.listAffinityGroupTypes(request)
	# result = api2.createAffinityGroup(request)
	print result
	# req = {'templatefilter':'featured','vpcid':'true'}
	# res = api.listTemplates(req)
	# rest = api.listNetworks(req)
	# rests = api.listServiceOfferings(request)
	# print len(result['virtualmachine'])
	# print "+++++++++++++++"
	# j = 0;
	# for i in result['virtualmachine']:
		# if 'displayname' in i.keys():
			# print i['displayname']
			# j+=1
	# print "#######"
	# print j
	# print result
	# print result['virtualmachine'][0]['hostname']
	# print result['virtualmachine']
	## print
	# print res
	# print rests
	## for i in result['virtualmachine']:
	##	# print i['nic'][0]['ipaddress']
# list()
