###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 13/01/2020.
###

import sys

from openpyweb.cmd import start
from openpyweb.cmd import server
from openpyweb.cmd import doc
from openpyweb.cmd import install
from openpyweb.cmd import help

if __name__ == '__main__':
    sys.exit(start.main(sys.argv[1:]))

if __name__ == '__main__':
    sys.exit(server.main(sys.argv[1:]))

if __name__ == '__main__':
    sys.exit(doc.main(sys.argv[1:]))

if __name__ == '__main__':
    sys.exit(install.main(sys.argv[1:]))

if __name__ == '__main__':
    sys.exit(help.main(sys.argv[1:]))

