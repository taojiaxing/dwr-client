## dwr-client
python direct web remoting client

required `requests`
### Start 
```python
DWR_HOST = 'https://www.example.com'
DWR_PARAMS = {'callCount':'1',
                'nextReverseAjaxIndex':'0',
                'c0-id':'0',
                'instanceId':'0'}
dwr = DWRClient(requests.Session(), DWR_HOST)
dwr.set_params(DWR_PARAMS)
dwr.set_page(DWR_HOST) #set page in dwr params
```

### Initialize
initialize dwr.

get session id and set session.
* script : script name default : `__System`
* method : method name default : `generateId`
```python
dwr.init()
```


### Dump Parameters
convert dictionary params to dwr param string.

return dwr params string

* params : dictionary ex) `{‘callCount’:’1’}`
```python
dwr.dumps({'a':'1', 'b':'2' })
```
return string
```
a=1
b=2
```

### Next Callflow
initialize `batchId=0`

reset session for another callflow
```python
dwr.reset()
```

### Set page
* page : string ex) `’/path/name'`
```python
dwr.set_page('/path/name') 
```

### Request to DWR
* script : script name 
* method : method name
* args : arguments list  with converting `string:` ex) `[‘0’, ‘1’]` 
* extra_params : add params which set using set_params() in this request
* url : url (optional) default : `/dwr/call/plaincall/script.method`
```python
dwr.request('dwrScript','method', ['1','2'])
```
return requests response

### Call DWR
same request params
* script : script name 
* method : method name
* args : arguments list  with converting `string:` ex) `[‘0’, ‘1’]` 
* extra_params : add params which set using set_params() in this request
* url : url (optional) default : `/dwr/call/plaincall/script.method`
```python
dwr.call('dwrScript','method', ['1','2'])
```
return dwr result parsing callback output

### Example
```python
DWR_HOST = 'https://www.example.com'
DWR_PARAMS = {'callCount':'1',
                'nextReverseAjaxIndex':'0',
                'c0-id':'0',
                'instanceId':'0'}
dwr = DWRClient(requests.Session(), DWR_HOST)
dwr.set_params(DWR_PARAMS)
dwr.set_page(DWR_HOST) #set page in dwr params
dwr.init()
res = dwr.request('dwrScript','method', ['1','2'])
'''
<Response [200]>

print(res.content)
>>>throw '~~~
dwr.engine.remote.handleCallback("0", "0", "
RESULT");
'''
dwr.call('dwrScript','method', ['1','2'])
'''
"RESULT"
'''
dwr.call('dwrScript','method1', ['1','2'])

dwr.set_page('/script/')
dwr.reset()
dwr.call('dwrScript1','method', ['1','2'])
``` 