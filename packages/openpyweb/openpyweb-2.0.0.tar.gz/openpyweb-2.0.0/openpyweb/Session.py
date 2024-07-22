###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###


import os
import datetime, time
import sys
import ast
from openpyweb.Version import *
from openpyweb.Log import Log
from openpyweb.util.Variable import Variable
from openpyweb.util.Crypt import Crypt


try:
    from http import cookies as cook
except Exception as err:
    import Cookie as cook


class Session(Variable):
    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None

    def __init__(self):
        self.result = ""
        self.s_string = "HTTP_COOKIE"
        self.session_list = []
        self._commit = []
        
        return None

    def has(self, key=""):
        bool_v = False
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            session_dict = self._get()
            if len(session_dict) > 0:
                if session_dict.get(key, "") != "":
                    bool_v = True
                elif session_dict.get(' {key}'.format(key=key), "") != "":
                    bool_v = True
                else:
                    bool_v = False
            else:
                bool_v = False
        else:

            if self.get(key) != "" and self.get(key) != None:

                bool_v = True
            else:
                bool_v = False

        return bool_v

    def set(self, key="", value="", duration=3600, url="", path="/",  samesite="", httponly=False, secure=False, max_age="", encrypt = False):
        _value = Crypt._encode(value) if encrypt == True else value
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            session_string = str(key) + "=" + _value
            return self._xset(session_string)
        else:
            return self._set(key, _value, duration, url, path, samesite, httponly, secure, max_age)
        

    def _set(self, key="", value="", duration=3600, url="", path="/", samesite="", httponly=False, secure=False, max_age="")->bool:
        
        url_v = self.out("HTTP_HOST") + str(":") + str(self.out("SERVER_PORT", '')) if self.out(
            "HTTP_HOST") == "localhost" or self.out("HTTP_HOST") == "127.0.0.1" else self.out("HTTP_HOST")
        url = url if url != "" else url_v
        expires = datetime.datetime.now(
        datetime.UTC) + datetime.timedelta(minutes=duration)
        cooKeys = cook.SimpleCookie(self.out(self.s_string))
        cooKeys[str(key)] = value
        cooKeys[str(key)]['domain'] = url
        cooKeys[str(key)]['path'] = path
        cooKeys[str(key)]['samesite'] = samesite
        cooKeys[str(key)]['httponly'] = httponly
        cooKeys[str(key)]['secure'] = secure
        cooKeys[str(key)]['max-age'] = max_age
        cooKeys[str(key)]['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S')
        print(cooKeys[str(key)])
        time.sleep(1)
        return True

    def get(self, key=""):
        if self.out("SERVER_SOFTWARE") == AUTHOR:
            session_dict = self._get()

            if len(session_dict) > 0:
                if session_dict.get(key, "") != None or session_dict.get(key, "") != "":
                    
                    if Crypt._isbase(session_dict.get(key, "")) == True:
                        try:
                            return ast.literal_eval(Crypt._decode(session_dict.get(key, "")))
                        except Exception as err:
                            return Crypt._decode(session_dict.get(key, ""))
                    else:
                        return session_dict.get(key, "")
                        
                elif session_dict.get(' {key}'.format(key=key), "") != None or session_dict.get(
                        ' {key}'.format(key=key), "") != "":
                    
                    if Crypt._isbase(session_dict.get(' {key}'.format(key=key), "")) == True:
                        try:
                            return ast.literal_eval(Crypt._decode(session_dict.get(' {key}'.format(key=key), "")))
                        except Exception as err:
                            return Crypt._decode(session_dict.get(' {key}'.format(key=key), ""))
                    else:
                        return session_dict.get(' {key}'.format(key=key), "")
                else:
                    return ""
            else:
                return ""
        else:
            cooKeys = cook.SimpleCookie()
            OsEnviron = self.out(self.s_string)
            if OsEnviron != None:
                cooKeys.load(OsEnviron)
                if key in cooKeys:

                    if cooKeys[key].value != None or cooKeys[key].value != "":
                        
                        if Crypt._isbase(cooKeys[key].value) == True:
                            try:
                                return ast.literal_eval(Crypt._decode(cooKeys[key].value))
                            except Exception as err:
                                return Crypt._decode(cooKeys[key].value)
                        else:
                            return cooKeys[key].value
                    else:
                        return ""
                else:
                    return ""
            else:
                return ""

    def destroy(self, key="", path= "/"):
        bool_v = False
        if self.out("SERVER_SOFTWARE") == AUTHOR:

            session_result = self._delete(key)
            if session_result[0] == True:
                self._reset(session_result[1])
                bool_v = True
            else:
                bool_v = False

        else:
            cooKeys = cook.SimpleCookie(self.out(self.s_string))
            if PYVERSION_MA >= 3:

                cookv = cooKeys.items()
            else:
                cookv = cooKeys.iteritems()

            self.out(self.s_string)

            bool_vx = False
            if self.s_string in os.environ:
                if key !="":
                    
                    if self.get(key) != "":
                        duration = 3600 * 30 * 1000
                        self._set(key=key, duration=-duration, path=path)
                        bool_vx = True
                    bool_v = bool_vx

                else:

                    for key, v in cookv:

                        if self.get(key) != "":
                            duration = 3600 * 33 * 1000

                            self._set(key=key, duration=-duration)
                            bool_vx = True
                    bool_v = bool_vx
            else:
                bool_v = False
        return bool_v

    def _xset(self, session_string=""):
        if session_string != "":
            if self.s_string not in self.see():
                self.default(self.s_string, session_string)

            else:
                self.session_list.append(session_string)
                self._update(self.unqiue(self.session_list))
        else:
            return False

    def _update(self, session_string):
        dict_session = dict({self.s_string: session_string})
        try:
            self.update(dict_session)
            return True
        except Exception as e:
            return False

    def unqiue(self, session_list=[]):

        session_relist = []
        for l_session in session_list:
            session_string = str(l_session) + ";" + str(self.out(self.s_string, "")
                                                        ) if self.out(self.s_string, "") != "" else str(l_session)
            session_relist.append(session_string)

        initial_session = str(session_relist).replace("[' ", "").replace("]", "").replace(',', ";").replace("'",
                                                                                                            "").replace(
            "[", "")
        return self._unquie(initial_session)

    def _unquie(self, initial_session=""):
        try:
            unique_session = initial_session.split(";")
            re_unique = []
            [re_unique.append(x) for x in unique_session if x not in re_unique]

            return ";".join(re_unique)
        except Exception as err:
            return initial_session

    def _delete(self, session_key=""):

        get_session = self._get()
        response = None
        if len(get_session) > 0:
            if len(session_key) > 0:

                try:
                    get_session.pop(session_key, None)
                    self._update(get_session)
                    response = True

                except Exception as err:
                    response = False
            else:
                try:
                    for k in dict(get_session):
                        get_session.pop(k, None)
                    response = True
                except Exception as err:
                    response = False
        else:
            response = False
        return response, get_session

    def _reset(self, session_dict=dict()):

        session_list = []
        if PYVERSION_MA >= 3:
            session_dict_l = session_dict.items()
        else:
            session_dict_l = session_dict.iteritems()

        for k, v in session_dict_l:
            session_list.append("{k}={v}".format(k=k, v=v))

        return self._update(";".join(session_list))

    def _get(self):

        session_dict = {}
        session_string = ""
        try:
            session_string = self.out(self.s_string)
        except Exception as err:

            session_dict = {}
        try:
            for c_g in session_string.split(";"):
                k, v = c_g.split("=")
                session_dict.update({str(k): str(v)})
        except Exception as err:
            try:
                k, v = session_string.split("=")
                session_dict.update({str(k): str(v)})
            except Exception as err:
                session_dict = {}
        return session_dict

    
