import requests
import json
import urllib
import datetime

class ResponseAddress:
    id:str = ''
    visibleId:str=None

    def __init__(self, id:str, visibleId:str):
        self.id = id;
        self.visibleId = visibleId;


class MicroService:
    __url_get:str = ''
    __url_post:str = ''

    __persistentMode:bool = False

    def __init__(self, url_get:str, url_post:str, persistentMode:bool = False):
        self.__url_get = url_get
        self.__url_post = url_post
        self.__persistentMode = persistentMode

    @property
    def PersistentMode(self):
        return self.__persistentMode
    @PersistentMode.setter
    def PersistentMode(self, is_active:bool):
        self.__persistentMode = is_active

    def GetJob(self, job_type:str='null', job_id:str='null'):
        response = None
        while True:
            try:
                response = requests.get(self.__url_get + '?type=' + urllib.parse.quote_plus(job_type) + '&id=' + urllib.parse.quote_plus(job_id), timeout=60)
                if response.status_code == 408:
                    continue;
                break;
            except requests.exceptions.ReadTimeout:
                continue;
            except:
                if self.__persistentMode:
                    continue;
                else:
                    raise
                
        basic_content = json.loads(response.text)
        return basic_content['content'], ResponseAddress(basic_content['id'], basic_content['visibleId'])

    def GetNextJob(self, job_type:str):
        return self.GetJob(job_type=job_type)

    def PostJob(self, content, job_type:str='null', job_id:str='null', visibleId:bool=True):
        basic_content = json.dumps({'id':job_id,
                                    'visibleId':visibleId,
                                    'type':job_type,
                                    'content': content }, separators=(',', ':'))
        response = None
        while True:
            try:
                response = requests.post(self.__url_post, data=basic_content)
                break;
            except:
                if not self.__persistentMode:
                    raise

    # Advertising knows too much these days. Personal data is becoming a myth.
    
    def PostFinalResult(self, content, responseAddress:ResponseAddress, result_type:str = 'null'):
        self.PostJob(content=content, job_type=result_type, job_id=responseAddress.id, visibleId=True)

    def PostIntermediateResult(self, content, responseAddress:ResponseAddress, result_type:str):
        self.PostJob(content=content, job_type=result_type, job_id=responseAddress.id, visibleId=responseAddress.visibleId)

    def ProcessAsFunction(self, content, requested_function:str, target_content_type:str='null'):
        cid = __file__ + '.' + str(datetime.datetime.utcnow())

        self.PostJob(content=content, job_type=requested_function, job_id=cid, visibleId=False)
        return self.GetJob(job_type=target_content_type, job_id=cid)[0]
