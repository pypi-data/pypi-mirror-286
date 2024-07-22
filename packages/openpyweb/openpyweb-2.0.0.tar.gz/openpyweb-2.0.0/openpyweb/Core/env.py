###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2/24/20.
###

import os

class env:



    def __init__(self):
        return None

    def _e(self):
        

        if os.path.isdir(os.path.join(os.getcwd(), 'public')):
            host = os.getcwd()  # os.path.dirname(os.getcwd())

        else:
            host = os.path.dirname(os.getcwd())

        DS = str("/")

        envpath = host + DS + ".env"

        if os.path.isfile(envpath) == True:

            try:
                ##f = open(envpath, "r")
                return self._s(envpath)#f.read()
            except Exception as err:
                   print(err)
        else:
            print(".env file not found")


    def _s(self, env_file):

        f = open(env_file, "r")
        splt = f.read()
        env_vars = {}
        rd, rds = "", ""

        for ls in splt.split():

            if ls.startswith('#') or not ls.strip():
                continue
            try:

                k, v = ls.split("=")
                env_vars.update({k: v})
            except Exception as err:
                rd += ls

        brack_f = str(rd)[1:]
        brack_e = brack_f[:-1]
        rds += '{'+str(brack_e)+"," + str(env_vars)[1:][:-1] if len(env_vars) > 0 else '{'+brack_e
        rds += '}'

        return rds