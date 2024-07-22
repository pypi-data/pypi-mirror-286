###
# Author : Emmanuel Essien
# Author Email : emmanuelessiens@outlook.com
# Maintainer By: Emmanuel Essien
# Maintainer Email: emmanuelessiens@outlook.com
# Created by Emmanuel Essien on 2019.
###


import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

from openpyweb import App, Log
log_msg = Log.Log()

class SMTP(App.App):

    def __init__(self):
        
        self.setting = self.envrin('SMTP')
        self.server = self.setting.get('server', '')
        self.port = self.setting.get('port', '')
        self.username = self.setting.get('username', '')
        self.password = self.setting.get('password', '')

        self.con = None
        self.result = None
        self.response = None
        self.attachfile = None
        return None

    def connect(self):
        try:
            self.response = smtplib.SMTP_SSL(self.server, self.port)
            self.response.login(self.username, self.password)
            return self.response
        except Exception as err:
            log_msg.error(err)
            return None


    def close(self):
        return self.response.quit()


    def send(self, from_send, to_recipient, message_subject= "", messege_content = "", header="html"):
        
        try:
            if self.connect() != None:
                body = messege_content
                msg = MIMEMultipart()
                msg['From'] = from_send
                msg['To'] = to_recipient
                msg['Subject'] = message_subject
                msg.attach(MIMEText(body, header))
                if self.attachfile != None:
                    msg.attach(self.attachfile)

                context = msg.as_string()
                self.response.sendmail(from_send, to_recipient, context)
                self.close()
                return True
            else:
                log_msg.error("No Smtp connection establish")
                return False
        except Exception as err:
            log_msg.error(err)
            return False

    def attach(self, atfile = "", rename=""):
        if atfile != "":
            try:
                ext = os.path.splitext(atfile)[1][1:]
                filename = atfile if rename == "" else str(rename) + '.' + str(ext)
                attach_file = open(atfile, 'rb')
                attach_load = MIMEBase('application', 'octet-stream')
                attach_load.set_payload(attach_file.read())
                encoders.encode_base64(attach_load)
                attach_load.add_header('Content-Disposition', 'attachment', filename=filename)
                self.attachfile = attach_load

            except Exception as err:
                try:
                    ext =  os.path.splitext(atfile.filename)[1][1:]
                    filename = atfile.filename if rename == "" else str(rename)+'.'+str(ext)
                    attach_load = MIMEBase('application', 'octet-stream')
                    read_attach_file = (atfile.file).read()
                    attach_load.set_payload(read_attach_file)
                    encoders.encode_base64(attach_load)
                    attach_load.add_header('Content-Disposition', 'attachment',  filename=filename)

                    self.attachfile = attach_load

                except Exception as err:

                    log_msg.error(err)

        return self


    def retrieve(self):
        return self.response.getreply()