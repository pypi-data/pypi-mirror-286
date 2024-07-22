###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 08/11/2019.
###
from openpyweb.App import App



class Schema(App):

    def __getattr__(self, item):
        return item


    def __init__(self):
        return None

    def table(self, table):
        self.DB()
        drive = self.Driver
        if drive == "MYSQL":
            from openpyweb.Driver.DB.MYSQL.Table import  Table
            return Table(table)

        if drive == "Oracle":
            from openpyweb.Driver.DB.Oracle.Table import  Table
            return Table(table)

        if drive == "pyPgSQL":
            from openpyweb.Driver.DB.pyPgSQL.Table import  Table
            return Table(table)

        if drive == "SQLite":
            from openpyweb.Driver.DB.SQLite.Table import  Table
            return Table(table)

    def raw(self, string):
        return string

    def query(self, raw):
        return self.DB().query(raw)

