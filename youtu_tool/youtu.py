# -*- coding: utf-8 -*-

import os.path
import time
import requests
import base64
import json
from youtu_tool import conf
from .auth import Auth

class YouTu(object):

    def __init__(self, appid, secret_id, secret_key, userid='0', end_point=conf.API_YOUTU_END_POINT):
        self.IMAGE_FILE_NOT_EXISTS = -1
        self.IMAGE_NETWORK_ERROR = -2
        self.IMAGE_PARAMS_ERROR = -3
        self.PERSON_ID_EMPTY = -4
        self.GROUP_ID_EMPTY  = -5
        self.GROUP_IDS_EMPTY = -6
        self.IMAGES_EMPTY    = -7
        self.FACE_IDS_EMPTY  = -8
        self.FACE_ID_EMPTY   = -9
        self.LIST_TYPE_INVALID = -10
        self.IMAGE_PATH_EMPTY = -11

        self.VALIDATE_DATA_EMPTY = -12
        self.VIDEO_PATH_EMPTY = -13
        self.CARD_PATH_EMPTY = -14
        self.IDCARD_NAME_OR_ID_EMPTY = -15

        self.VIDEO_FILE_NOT_EXISTS = -16
        self.CARD_FILE_NOT_EXISTS = -17

        self.UNKNOW_CARD_TYPE = -18
        
        self.EXPIRED_SECONDS = 2592000
        self._secret_id  = secret_id
        self._secret_key = secret_key
        self._appid      = appid
        self._userid     = userid
        self._end_point  = end_point
        conf.set_app_info(appid, secret_id, secret_key, userid, end_point)
    
    def get_headers(self, req_type):
       
        expired = int(time.time()) + self.EXPIRED_SECONDS
        auth = Auth(self._secret_id, self._secret_key, self._appid, self._userid)
        
        sign = auth.app_sign(expired)
        headers = {
                   'Authorization':sign,
                   'Content-Type':'text/json'
        }    
        
        return headers    
        
    def generate_res_url(self, req_type, url_type = 0):
        
        app_info = conf.get_app_info()
        url_api_str = '' 
        if url_type == 4:
            url_api_str = 'youtu/carapi'
        elif url_type == 3:
            url_api_str = 'youtu/openliveapi'
        elif url_type == 2:
            url_api_str = 'youtu/ocrapi'
        elif url_type == 1:
            url_api_str = 'youtu/imageapi'
        else :
            url_api_str = 'youtu/api'
            
        return app_info['end_point'] + url_api_str + '/' + str(req_type)
    
    def FaceCompare(self, image_pathA, image_pathB, data_type = 0):
        
        req_type = 'facecompare'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        data = {
            "app_id": self._appid
        }
        
        if len(image_pathA) == 0 or len(image_pathB) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', 'session_id':'', 'similarity':0}
       
        if data_type == 0:  
            filepathA = os.path.abspath(image_pathA)
            filepathB = os.path.abspath(image_pathB)
            
            if not os.path.exists(filepathA):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', 'session_id':'', 'similarity':0}
            if not os.path.exists(filepathB):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', 'session_id':'', 'similarity':0}
            
            data["imageA"] = base64.b64encode(open(filepathA, 'rb').read()).rstrip().decode('utf-8')
            data["imageB"] = base64.b64encode(open(filepathB, 'rb').read()).rstrip().decode('utf-8')
        else :
            data["urlA"] = image_pathA
            data["urlB"] = image_pathB
             
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':'', 'session_id':'', 'similarity':0}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0,  'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), 'session_id':'', 'similarity':0}
                
        return ret            
    
    def FaceVerify(self, person_id, image_path, data_type = 0):
       
        req_type='faceverify' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)

        data = {
            "app_id": self._appid,
            "person_id": person_id
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', "confidence":0, "ismatch":0, "session_id":''}
        
        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "confidence":0, "ismatch":0, "session_id":''}
            if len(person_id) == 0:
                return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY', "confidence":0, "ismatch":0, "session_id":''}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else :
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:  
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "confidence":0, "ismatch":0, "session_id":''}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "confidence":0, "ismatch":0, "session_id":''}
                
        return ret 
        
    def FaceIdentify(self, group_id, image_path, data_type = 0):
        
        req_type='faceidentify' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        data = {
            "app_id": self._appid
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', "session_id":'', "candidates":[{}]}
        
        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "session_id":'', "candidates":[{}]}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else :
            data["url"] = image_path
            
        if len(group_id) == 0:
            return {'httpcode':0, 'errorcode':self.GROUP_ID_EMPTY, 'errormsg':'GROUP_ID_EMPTY', "session_id":'', "candidates":[{}]}
        else :
            data["group_id"] = group_id
         
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:  
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "session_id":'', "candidates":[{}]}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "session_id":'', "candidates":[{}]}
                
        return ret 
    
    def MultiFaceIdentify(self, group_id, group_ids, image_path, data_type = 0, topn = 5, min_size = 40):
        
        req_type='multifaceidentify' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        data = {
            "app_id": self._appid,
            "topn": topn,
            "min_size": min_size
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', "session_id":'', "candidates":[{}]}
        
        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "session_id":'', "candidates":[{}]}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else :
            data["url"] = image_path
            
        if len(group_id) == 0 and len(group_ids) == 0:
            return {'httpcode':0, 'errorcode':self.ERROR_PARAMETER_EMPTY, 'errormsg':'ERROR_PARAMETER_EMPTY', "session_id":'', "candidates":[{}]}
        elif len(group_id) != 0:
            data["group_id"] = group_id
        else :
            data["group_ids"] = group_ids
         
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:  
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "session_id":'', "candidates":[{}]}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "session_id":'', "candidates":[{}]}
                
        return ret 

    def DetectFace(self, image_path, mode = 0, data_type = 0):
        
        req_type='detectface' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        data = {
            "app_id": self._appid,
            "mode": mode
        }
        
        # if len(image_path) == 0:
        #     return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', "session_id":'', "image_id":'', "image_height":0, "image_width":0, "face":[{}]}
                 
        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "session_id":'', "image_id":'', "image_height":0, "image_width":0, "face":[{}]}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else :
            data["url"] = image_path
         
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "session_id":'', "image_id":'', "image_height":0, "image_width":0, "face":[{}]}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "session_id":'', "image_id":'', "image_height":0, "image_width":0, "face":[{}]}
                
        return ret 
   
    
    def NewPerson(self, person_id, image_path, group_ids, person_name= '', tag='', data_type = 0):
        
        req_type='newperson' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY', "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}
        
        if len(group_ids) == 0:
            return {'httpcode':0, 'errorcode':self.GROUP_IDS_EMPTY, 'errormsg':'GROUP_IDS_EMPTY', "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}

        if type(group_ids) != list:
            return {'httpcode':0, 'errorcode': self.LIST_TYPE_INVALID, 'errormsg':'LIST_TYPE_INVALID', "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}
            
        data = {
            "app_id": self._appid,
            "person_id" : person_id,
            "person_name": person_name,
            "group_ids": group_ids,
            "tag": tag
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
            
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}
                
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "person_id":'', "suc_group":'', "suc_face":0, "session_id":0, "face_id":'', "group_ids":''}
                       
        return ret 
        
    def DelPerson(self, person_id) :  
        
        req_type='delperson' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY', "deleted":0, "session_id":''}
        
        data = {
            "app_id": self._appid,
            "person_id" : person_id 
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                 return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "deleted":0, "session_id":''}
                 
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "deleted":0, "session_id":''}
                 
        return ret 
    
    def AddFace(self, person_id, images, tag='', data_type = 0): 
        
        req_type='addface' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY', "face_ids":[], "session_id":'', "added": 0, "ret_codes":[]}
        
        data = {
            "app_id": self._appid,
            "person_id" : person_id,   
            "tag" : tag
        }
        
        if len(images) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGES_EMPTY, 'errormsg':'IMAGES_EMPTY', "face_ids":[], "session_id":'', "added": 0, "ret_codes":[]}
        
        if type(images) != list:
            return {'httpcode':0, 'errorcode':self.LIST_TYPE_INVALID, 'errormsg':'LIST_TYPE_INVALID', "face_ids":[], "session_id":'', "added": 0, "ret_codes":[]}
        
        if  data_type == 0:
            images_content = []
            for image in images:
                filepath = os.path.abspath(image)
                if not os.path.exists(filepath):
                    return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "face_ids":[], "session_id":'', "added": 0, "ret_codes":[]}
                
                images_content.append(base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8'))
            data["images"] = images_content
        else :
            data["urls"] = images
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                  return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "face_ids":[], "session_id":'', "added": 0, "ret_codes":[]}
                  
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "face_ids":[], "session_id":'', "added": 0, "ret_codes":[]}
                 
        return ret 
    
    def DelFace(self, person_id, face_ids):
        
        req_type='delface' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY',  "session_id":'', "deleted ": 0}
        
        if len(face_ids) == 0:
            return {'httpcode':0, 'errorcode':self.FACE_IDS_IMPTY, 'errormsg':'FACE_IDS_IMPTY',  "session_id":'', "deleted ": 0}
        
        if type(face_ids) != list:
            return {'httpcode':0, 'errorcode':self.LIST_TYPE_INVALID, 'errormsg':'LIST_TYPE_INVALID',  "session_id":'', "deleted ": 0} 
        
        data = {
            "app_id": self._appid,
            "person_id":person_id,
            "face_ids":face_ids
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'',  "session_id":'', "deleted ": 0}
                 
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e),  "session_id":'', "deleted ": 0}
                 
        return ret        
    
    
    def SetInfo(self, person_id, person_name='', tag=''):
        
        req_type='setinfo' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        url_type
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY',  "person_id":'', "session_id ": ''}
       
        data = {
            "app_id": self._appid,
            "person_id": person_id,
            "person_name": person_name,
            "tag":tag
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'',  "person_id":'', "session_id ": ''}
                
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e),  "person_id":'', "session_id ": ''}
                 
        return ret 
        
    def GetInfo(self, person_id):
    
        req_type='getinfo' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY',  "person_id":'', "person_name ": '', "face_ids":[], "tag":'', "secret_id":''}
        
        data = {
            "app_id": self._appid,
            "person_id": person_id
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'',  "person_id":'', "person_name ": '', "face_ids":[], "tag":'', "secret_id":''}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e),  "person_id":'', "person_name ": '', "face_ids":[], "tag":'', "secret_id":''}
                
        return ret 
    
    def GetGroupIds(self):
        
        req_type='getgroupids' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        data = {
            "app_id": self._appid
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'',  "group_ids":[]}
                
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "group_ids":[]}
                
        return ret
        
    def GetPersonIds(self, group_id) :
    
        req_type='getpersonids' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(group_id) == 0:
            return {'httpcode':0, 'errorcode':self.GROUP_ID_EMPTY, 'errormsg':'GROUP_ID_EMPTY', "person_ids":[]}

        data = {
            "app_id": self._appid,
            "group_id": group_id
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "person_ids":[]}    
                
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "person_ids":[]}
                
        return ret
    
    def GetFaceIds(self, person_id):
        
        req_type='getfaceids' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(person_id) == 0:
            return {'httpcode':0, 'errorcode':self.PERSON_ID_EMPTY, 'errormsg':'PERSON_ID_EMPTY',  "face_ids":[]}
        
        data = {
            "app_id": self._appid,
            "person_id": person_id
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'',  "face_ids":[]}  
                
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e),  "face_ids":[]}  
                
        return ret    
    
    def GetFaceInfo(self, face_id):
        
        req_type='getfaceinfo' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        if len(face_id) == 0:
            return {'httpcode':0, 'errorcode':self.FACE_ID_EMPTY, 'errormsg':'FACE_ID_EMPTY',  "face_info":[]}
        
        data = {
            "app_id": self._appid,
            "face_id": face_id 
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                 return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'',  "face_info":[]}   
                 
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e),  "face_info":[]}  
                
        return ret 
    
    def FaceShape(self, image_path, mode = 0, data_type = 0):
        
        req_type='faceshape' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type)
        
        data = {
            "app_id": self._appid,
            "mode": mode
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY', "face_shape":[{}], "image_height":0, "image_width":0, "session_id":''}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS', "face_shape":[{}], "image_height":0, "image_width":0, "session_id":''}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':'', "face_shape":[{}], "image_height":0, "image_width":0, "session_id":''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), "face_shape":[{}], "image_height":0, "image_width":0, "session_id":''}
                
        return ret
    
    def fuzzydetect(self, image_path, data_type = 0, seq = ''):
        
        req_type='fuzzydetect' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 1)
        
        data = {
            "app_id": self._appid,
            "seq": seq
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret
    
    def fooddetect(self, image_path, data_type = 0, seq = ''):
        
        req_type='fooddetect' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 1)
        
        data = {
            "app_id": self._appid,
            "seq": seq
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret
    
    

    def imagetag(self, image_path, data_type = 0, seq = ''):
    
        req_type='imagetag' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 1)
        
        data = {
            "app_id": self._appid,
            "seq": seq
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret
        
    def imageporn(self, image_path, data_type = 0, seq = ''):
    
        req_type='imageporn' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 1)
        
        data = {
            "app_id": self._appid,
            "seq": seq
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret
    
    def imageterrorism(self, image_path, data_type = 0, seq = ''):
    
        req_type='imageterrorism' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 1)
        
        data = {
            "app_id": self._appid,
            "seq": seq
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret

    def carclassify(self, image_path, data_type = 0, seq = ''):
    
        req_type='carclassify' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 4)
        
        data = {
            "app_id": self._appid,
            "seq": seq
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret

    def idcardocr(self, image_path, data_type = 0, card_type = 1 ,seq = ''):
    
        req_type='idcardocr' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        
        data = {
            "app_id": self._appid,
            "seq": seq,
            "card_type":card_type
        }
        
        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}
        
        if data_type == 0:    
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}
            
            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200: 
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}
  
            ret = r.json()          
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}
                
        return ret
    
    def driverlicenseocr(self, image_path, data_type = 0, proc_type = 0, seq = ''):

        req_type='driverlicenseocr'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        data = {
            "app_id": self._appid,
            "session_id": seq,
            "type": proc_type
        }

        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}

        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}

            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path

        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}

            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}

        return ret

    def bcocr(self, image_path, data_type = 0, seq = ''):

        req_type='bcocr'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        data = {
            "app_id": self._appid,
            "session_id": seq,
        }

        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}

        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}

            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path

        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}

            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}

        return ret

    def generalocr(self, image_path, data_type = 0, seq = ''):

        req_type='generalocr'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        data = {
            "app_id": self._appid,
            "session_id": seq,
        }

        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}

        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}

            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path

        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}

            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}

        return ret

    def creditcardocr(self, image_path, data_type = 0, seq = ''):

        req_type='creditcardocr'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        data = {
            "app_id": self._appid,
            "session_id": seq,
        }

        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}

        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}

            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path

        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}

            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}

        return ret

    def bizlicenseocr(self, image_path, data_type = 0, seq = ''):

        req_type='bizlicenseocr'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        data = {
            "app_id": self._appid,
            "session_id": seq,
        }

        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}

        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}

            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path

        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}

            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}

        return ret

    def plateocr(self, image_path, data_type = 0, seq = ''):

        req_type='plateocr'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 2)
        data = {
            "app_id": self._appid,
            "session_id": seq,
        }

        if len(image_path) == 0:
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY'}

        if data_type == 0:
            filepath = os.path.abspath(image_path)
            if not os.path.exists(filepath):
                return {'httpcode':0, 'errorcode':self.IMAGE_FILE_NOT_EXISTS, 'errormsg':'IMAGE_FILE_NOT_EXISTS'}

            data["image"] = base64.b64encode(open(filepath, 'rb').read()).rstrip().decode('utf-8')
        else:
            data["url"] = image_path

        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':'', 'errormsg':''}

            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e)}

        return ret

    def livegetfour(self, seq = ''):

        req_type = 'livegetfour'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 3)

        data = {
            'app_id' : self._appid,
            'seq' : seq
        }

        r = {}
        try:
            r = requests.post(url, headers = headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode' : r.status_code, 'errorcode' : '', 'errormsg' : '', 'validate_data' : ''}
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), 'validate_data' : ''} 

        return ret

    def livedetectfour(self, validate_data, video_path,  seq = '', card_path = '', compare_flag = False):

        req_type = 'livedetectfour' 
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 3)

        data = {
            'app_id' : self._appid,
            'seq' : seq
        }

        if len(validate_data) == 0:
            return {'httpcode' : 0, 'errorcode' : self.VALIDATE_DATA_EMPTY, 'errormsg' : 'VALIDATE_DATA_EMPTY', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}
        
        if len(video_path) == 0:
            return {'httpcode' : 0, 'errorcode' : self.VIDEO_PATH_EMPTY, 'errormsg' : 'VIDEO_PATH_EMPTY,', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}

        if compare_flag == True and len(card_path) == 0:
            return {'httpcode' : 0, 'errorcode' : self.CARD_PATH_EMPTY, 'errormsg' : 'CARD_PATH_EMPTY', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}

        videofile = os.path.abspath(video_path)
        if not os.path.exists(videofile):
            return {'httpcode' : 0, 'errorcode' : self.VIDEO_FILE_NOT_EXISTS, 'errormsg' : 'VIDEO_FILE_NOT_EXISTS', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}
        else:
            data["video"] = base64.b64encode(open(videofile, 'rb').read()).rstrip()


        cardfile = os.path.abspath(card_path)
        if compare_flag == True :
            if not os.path.exists(cardfile):
                return {'httpcode' : 0, 'errorcode' : self.CARD_FILE_NOT_EXISTS, 'errormsg' : 'CARD_FILE_NOT_EXISTS', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}
            else:
                 data["card"] = base64.b64encode(open(cardfile, 'rb').read()).rstrip()
        
        data['validate_data'] = validate_data
        data['compare_flag'] = compare_flag

        r = {}
        try:
            r = requests.post(url, headers = headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode' : r.status_code, 'errorcode' : '', 'errormsg' : '', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}
            ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'photo' : ''}

        return ret

    def idcardlivedetectfour(self, idcard_number, idcard_name, validate_data, video_path, seq = ''):

        req_type = 'idcardlivedetectfour'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 3)

        data = {
            'app_id' : self._appid,
            'seq' : seq
        }

        if len(idcard_name) == 0 or len(idcard_number)  == 0:
            return {'httpcode' : 0, 'errorcode' : self.IDCARD_NAME_OR_ID_EMPTY , 'errormsg' : 'IDCARD_NAME_OR_ID_EMPTY ', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'video_photo' : ''}

        if len(validate_data) == 0:
            return {'httpcode' : 0, 'errorcode' : self.VALIDATE_DATA_EMPTY, 'errormsg' : 'VALIDATE_DATA_EMPTY', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'video_photo' : ''}
        
        if len(video_path) == 0:
            return {'httpcode' : 0, 'errorcode' : self.VIDEO_PATH_EMPTY, 'errormsg' : 'VIDEO_PATH_EMPTY', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'video_photo' : ''}

        videofile = os.path.abspath(video_path)
        if not os.path.exists(videofile):
            return {'httpcode' : 0, 'errorcode' : self.VIDEO_FILE_NOT_EXISTS, 'errormsg' : 'VIDEO_FILE_NOT_EXISTS', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'video_photo' : ''}
        else:
            data["video"] = base64.b64encode(open(videofile, 'rb').read()).rstrip()

        data['idcard_number'] = idcard_number
        data['idcard_name'] = idcard_name
        data['validate_data'] = validate_data

        r = {}
        try:
             r = requests.post(url, headers = headers, data = json.dumps(data))
             if r.status_code != 200 :
                return {'httpcode' : r.status_code, 'errorcode' : '', 'errormsg' : '', 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'video_photo' : ''}
             ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), 'live_status' : '', 'live_msg' : '', 'compare_status' : '', 'compare_msg' : '', 'sim' : 0, 'video_photo' : ''}

        return ret

    def idcardfacecompare(self, idcard_number, idcard_name, image_path, data_type = 0 , session_id = ''):

        req_type = 'idcardfacecompare'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 3)

        data = {
            'app_id' : self._appid,
            'session_id' : session_id
        }

        if len(idcard_name) == 0 or len(idcard_number) == 0 :
            return {'httpcode' : 0, 'errorcode' : self.IDCARD_NAME_OR_ID_EMPTY , 'errormsg' : 'IDCARD_NAME_OR_ID_EMPTY ', 'similarity' : '', 'session_id' : session_id}
        
        if len(image_path) == 0 :
            return {'httpcode':0, 'errorcode':self.IMAGE_PATH_EMPTY, 'errormsg':'IMAGE_PATH_EMPTY',  'similarity' : '', 'session_id' : session_id}

        if data_type == 0:
            imagefile = os.path.abspath(image_path)
            if not os.path.exists(imagefile):
                return {'httpcode' : 0, 'errorcode' : self.IMAGE_FILE_NOT_EXISTS, 'errormsg' : 'IMAGE_FILE_NOT_EXISTS', 'similarity' : '', 'session_id' : session_id}
            else:
                data['image'] = base64.b64encode(open(imagefile, 'rb').read()).rstrip()
        else:
            data['url'] = image_path
        data['idcard_number'] = idcard_number
        data['idcard_name'] = idcard_name

        r = {}
        try:
             r = requests.post(url, headers = headers, data = json.dumps(data))
             if r.status_code != 200:
                return {'httpcode' : r.status_code, 'errorcode' : '', 'errormsg' : '', 'similarity' : '', 'session_id' : session_id}
             ret = r.json()
        except Exception as e:
            return {'httpcode':0, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), 'similarity' : '', 'session_id' : session_id}

        return ret
    
    def ValidateIdcard(self, idcard_number, idcard_name, seq = "default"):
        
        req_type = 'validateidcard'
        headers = self.get_headers(req_type)
        url = self.generate_res_url(req_type, 3)
        
        data = {
            "app_id": self._appid,
            "idcard_number": idcard_number,
            "idcard_name": idcard_name,
            "seq": seq
        }
        
        r = {}
        try:
            r = requests.post(url, headers=headers, data = json.dumps(data))
            if r.status_code != 200:
                return {'httpcode':r.status_code, 'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':'', 'session_id':''}
            ret = r.json()
            
        except Exception as e:
            return {'httpcode':0,  'errorcode':self.IMAGE_NETWORK_ERROR, 'errormsg':str(e), 'session_id':''}
                
        return ret
    
   
