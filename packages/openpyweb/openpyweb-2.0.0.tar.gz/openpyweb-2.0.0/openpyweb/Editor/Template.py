###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###

from openpyweb.Editor.Compiler import Compiler

class Template(object):
    def __init__(self, contents):
        self.contents = contents
        self.root = Compiler(self.contents).compile()

    def render(self, **kwargs):
        
        return str(self.root.render(kwargs)).replace('\ufeff', ' ').replace('\u20a6', ' ')