###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###
def Model():
    from . import Model
    return Model


Model().auto()


def App():
    from . import App
    return App.App()


def Version():
    from . import Version as vern
    return vern


def Config():
    from . import Config as Config
    return Config.Config()


def Helpers():
    from .Core import Helpers
    return Helpers


def Session():
    from .Session import Session
    return Session()


def Request():
    from .Request import Request
    return Request()


def Hash():
    from .Hash import Hash
    return Hash()

def Load(m):
    return Model().Model().load(m)


def Functions():
    from .Core import Functions
    return Functions

def SMTP():
    from .Core.SMTP import SMTP
    return SMTP()

def Pagination():
    from .Functions.pagination import pagination
    return pagination()


def Validation():
    from .Functions.validation import validation
    return validation()


def Curl():
    from .Functions.curl import curl
    return curl()


def Now():
    from .Functions.now import now
    return now()


def Os():
    from .Functions.agent import os
    return os()


def browser():
    from .Functions.agent import browser
    return browser()


def extend():
    from .Functions.extend import extend
    return extend()


def path():
    from .Functions.path import path
    return path()

def Rand():
    from .Functions.rand import rand
    return rand()

def include():
    from .Functions.include import include
    return include


def File():
    from .Core import File
    return File()


def SendEmail(from_send, to_recipient, message_subject="", messege_content=""):
    from .Core.SMTP import SMTP

    return SMTP().send(from_send, to_recipient, message_subject, messege_content)

def mailer():
    from .Core.SMTP import SMTP

    return SMTP()


def Logs():
    from .Log import Log

    return Log()


def url(path="", lang=False):
    from .Functions.url import url
    return url(path, lang)


def env(key):

    return App().envrin(key)

def encode(source):
    from .util.Crypt import Crypt
    return Crypt._encode(source)

def decode(source):
    from .util.Crypt import Crypt
    return Crypt._decode(source)

def Schema():
    from .Driver import Schema
    return  Schema.Schema()