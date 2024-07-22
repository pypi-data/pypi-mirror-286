###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 05/11/2019.
###
import os
from openpyweb.util.Variable import Variable
from openpyweb.Router import Router
from openpyweb.Controllers import Controllers
from openpyweb import Version


class url(Variable):
    def __getattr__(self, item):
        return item

    def __call__(self, *args, **kwargs):
        return None

    def __init__(self, *args, **kwargs):

        if len(args) > 0 or len(kwargs) > 0:

            if all(args) is not False:
                self.ul = self.url(*args, **kwargs)
            else:
                self.ul = self.url(**kwargs)
        else:
            self.ul = self.url(*args)
        
        return None

    def __str__(self):

        return self.ul


    def __join(self, *uris) -> str:
        """
        Joins the URIs carefully considering the prefixes and trailing slashes.
        The trailing slash for the end URI is handled separately.
        """
        if len(uris) == 1:
            return uris[0]

        safe_urls = [
            f"{url.lstrip('/')}/" if not url.endswith("/") else url.lstrip("/")
            for url in uris[:-1]
        ]
        safe_urls.append(uris[-1].lstrip("/"))
        return "".join(safe_urls)

    def url(self, path="", lang=False):

        p = ""
        self.Controllers = Controllers()
        seturl = self.out("HTTP_HOST")+str(":")+str(self.out("SERVER_PORT", '')) if self.out("HTTP_HOST") == "localhost" or self.out("HTTP_HOST") == "127.0.0.1" else self.out("HTTP_HOST")

        if self.out("HTTPS", "") == 'on':
            url = str("https://") + seturl.replace(":80", "") + "/" + self.Controllers.all_languages.get(self.Controllers._getLanguages(), self.Controllers.languages) if lang == True else str("https://") + seturl.replace(":80", "") 
        else:

            url = str("http://") + seturl.replace(":80", "")+ "/" + self.Controllers.all_languages.get(self.Controllers._getLanguages(), self.Controllers.languages) if lang == True else str("http://") + seturl.replace(":80", "")
        
        if path != "":
            if path[:1] == "/":
                p = str(path[1:])
            else:
                p = path
        
        return self.__join(url, p)
