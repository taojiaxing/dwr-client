import re
import random
import time

class DWRClient():
    batch_id = 0
    session = None
    is_initialized = False
    page = ''
    host = ''
    CALL_PATH = '/dwr/call/plaincall/'
    params = {}
    script_session_id = ''
    dwr_session = ''

    def __init__(self, session, host):
        self.session = session
        self.host = host
    
    def dumps(self, params):
        s_params = ''
        for key, value in params.items():
            s_params += '{0}={1}\n'.format(key, value)
        return s_params
    
    def tokenify(self, number): 
        tokenbuf = []
        charmap = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ*$"
        remainder = int(number)
        while remainder > 0:
            tokenbuf.append(charmap[remainder & 0x3F])
            remainder = int(remainder / 64)
        return ''.join(tokenbuf)

    def set_page_id(self):
        page_id1 = self.tokenify(time.time() * 1000)
        page_id2 = self.tokenify(random.random()* 1e16)
        self.page_id = '{0}-{1}'.format(page_id1, page_id2)
        return self.page_id
        
    def set_session(self, session):
        page_id = self.set_page_id()
        self.script_session_id = '{0}/{1}'.format(session, page_id)
    
    def reset(self):
        self.batch_id = 0
        self.set_session(self.dwr_session)
        
    def set_params(self, params):
        self.params = params

    def set_page(self, page):
        self.page = page

    def request(self, script, method, args=[], extra_params={}, url=''):
        if not self.is_initialized:
            raise 'not be Initialized'

        if not self.page:
            raise 'page is not be set, please set params using set_params()'

        datas = dict(self.params)
        for key, value in extra_params:
            datas[key] = value
        for i, arg in enumerate(args):
            if isinstance(arg, str):
                arg = 'string:{0}'.format(arg)
            datas['c0-param{0}'.format(i)] = arg
        
        datas['page'] = self.page.replace('/','%2F') #no quote
        datas['batchId'] = self.batch_id
        datas['scriptSessionId'] = self.script_session_id
        datas['c0-scriptName'] = script
        datas['c0-methodName'] = method
        if not url:
            url = self.host + self.CALL_PATH + script + '.' + method + '.dwr'
        data = self.dumps(datas)
        res = self.session.post(url, data=data)
        self.batch_id += 1
        return res
    
    def call(self, script, method, args=[], extra_params={}, url=''):
        res = self.request(script, method, args, extra_params, url)
        s = res.content.decode('utf-8')
        s = re.findall(r'handleCallback\("\w+",\s*"\w+",\s*"(.+?)"\);',s)
        return s[0]
    

    def init(self, script='__System', method='generateId', url=''):
        if not self.params:
            raise 'params is not be set, please set params using set_params()'
        self.batch_id = 0
        self.is_initialized = True
        self.dwr_session = self.call(script, method) 
        self.session.cookies['DWRSESSIONID'] = self.dwr_session
        self.set_session(self.dwr_session)
        return True