import urllib2
import requests as req
import json
import re
import os
import sys
from Galactic_Warships.conf import galacticwarships as CONFIG



class SALTDEPLOY(object):
    
    def __init__(self):
        self.__salt_url = CONFIG.SALT_API
        self.__salt_user = CONFIG.SALT_USER
        self.__salt_password = CONFIG.SALT_PASSWORD
        self.__salt_client = CONFIG.SALT_CLIENT
        self.__salt_func = CONFIG.SALT_FUNCTION
        self.__salt_func_arg = CONFIG.SALT_FUNC_ARG
        self.__salt_target_type = CONFIG.SALT_TARGET_TYPE
        self.__salt_target = CONFIG.SALT_TARGET
        self.__salt_auth_type = CONFIG.SALT_AUTH_TYPE

        print "salt_url: %s"%(CONFIG.SALT_API,)
        print "salt_user: %s"%(CONFIG.SALT_USER,)
        print "salt_passwd: %s"%(CONFIG.SALT_PASSWORD,)
        print "salt_function: %s"%(CONFIG.SALT_FUNCTION,)
        print "salt_auth_type: %s"%(CONFIG.SALT_AUTH_TYPE,)

    def __SaltApiLogin(self):
        reqLoginResult = req.post("%s/login"%(self.__salt_url,), data={'username':self.__salt_user, 'password':self.__salt_password, 'eauth':self.__salt_auth_type}, headers={'Accept':'application/json'})
        #requests.post('http://10.134.56.83:8000/login', data={'username':'salt_api', 'password':'salt_api', 'eauth':'pam'}, headers={'Accept':'application/x-yaml'})
        return reqLoginResult.json()

    def __GetToken(self):
        loginInfo = self.__SaltApiLogin()
        print type(loginInfo)
        print loginInfo
        return loginInfo['return'][0]['token']
        
    #def RunCmd(self, cmdclient = self.__salt_client, cmdtarget = self.__salt_target, cmdfunc = self.__salt_func, cmdarg = self.__salt_func_arg):
    def RunCmd(self, cmdtarget, pkgname):
        params={'client': self.__salt_client, 'tgt':"%s*"%(cmdtarget,), 'fun':self.__salt_func, 'arg':"%s %s"%(self.__salt_func_arg, pkgname)}
        #params={'client': self.__salt_client, 'tgt':self.__salt_target, 'fun':self.__salt_func, 'arg':self.__salt_func_arg}
        #params={'client': self.__salt_client, 'tgt':self.__salt_target, 'fun':self.__salt_func}
        #params={'client': cmdclient, 'tgt':cmdtarget, 'fun':cmdfunc, 'arg':cmdarg}
        token=self.__GetToken()
        print token
        print params
        head={'Accept':'application/json', 'X-Auth-Token':token}
        reqRunResult = req.post(self.__salt_url, data=params, headers=head)
        return reqRunResult.text

