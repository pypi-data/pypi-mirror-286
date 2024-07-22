###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###


from openpyweb.Version import *
import base64

class Crypt:

    def __getattr__(self, item):
        return item

    def __init__(self):
        
        return None

    @staticmethod
    def _isbase(sb):
        try:
            if isinstance(sb, str):
                # If there's any unicode here, an exception will be thrown and the function will return false
                sb_bytes = bytes(sb, 'ascii')
            elif isinstance(sb, bytes):
                sb_bytes = sb
            else:
                #raise ValueError("Argument must be string or bytes")
                return False
            return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
        except Exception:
            return False
        
    @staticmethod
    def _encode(source):
        from openpyweb.Functions.now import now
        from openpyweb.Functions.rand import rand
        from openpyweb.Hash import Hash
        sessionRAND =  Hash().hex_hash(rand().number(8), hex_type="{}".format(HASH_PRE["64"]), size=120)
        sessionTIMER = Hash().hex_hash(now().unix(), hex_type="{}".format(HASH_PRE["192"]), size=80)
        
        try:
            import six
            if six.PY3:
                source = str(sessionPREFIX+sessionRAND+str(source)+str(sessionTIMER)).encode('utf-8')
            content = base64.b64encode(source).decode('utf-8')
            return str(content)
        except Exception as err:
            return str(content)

    @staticmethod
    def _decode(source):
        try:
            import six
            import base64
            source = base64.b64decode(str(source)).decode()
            source = source.split("::")
            source = source[1][64:-192]
            try:
                return source if isinstance(int(source), int) == True else source
            except Exception as err:
                return source
        except Exception as err:
            return source