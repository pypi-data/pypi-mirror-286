###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###

import os
from openpyweb import Log
from openpyweb import Version
from openpyweb.Controllers import Controllers
from openpyweb import Router
import ast

log_msg = Log.Log()


class Lang:

    def __init__(self, lg):
        self.data = ""
        self.lg = lg
        

    def loadLang(self):
        if os.path.isdir(os.getcwd() + '/public'):
            host = os.getcwd()  # os.path.dirname(os.getcwd())

        else:
            host = os.path.dirname(os.getcwd())

        DS = str("/")
        ront = Controllers()
        getl = ront.all_languages
        
        langpath = host + DS + 'lang'+DS + \
            getl.get(self.lg.lower(), self.lg.lower()) + ".py"
        
        try:
            if os.path.isfile(langpath) == True:

                with open(langpath, 'rb') as rb:
                    self.data = rb.read().decode('utf-8')
                
                return self.data

        except Exception as e:
            log_msg.error("Lang file not found {}".format(e))
            return "Lang file not found {}".format(e)

    def get(self, key, defindValue=''):

        data = ast.literal_eval(self.data)

        return data.get(key.lower(), defindValue)
