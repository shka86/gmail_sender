#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from os.path import basename

import csv

from getpass import getpass


# # windowsの場合はコレ↓しとかないとエラー出るか？
# import locale
# locale.setlocale(locale.LC_ALL, '')

class MailSettings:
    def __init__(self):
        self.mailfrom = ""
        self.mailcc = ""
        self.mailbcc = ""
        self.mailsub = ""
        self.mailpass = ""
        self.mailtemplate = ""
        self.mailbody = ""
        self.mailattach = ""
        self.to_names = []
        self.to_addrs = []
        self.if_sends = []

        self.get_send_list()
        self.get_mail_settings()
        self.get_sender_password()
        self.get_mail_template()
        self.get_attachment()

    def get_send_list(self):
        with open('sendlist.csv', 'r') as f:
            sendlist = f.readlines()[1:]

        for row in sendlist:
            row = row.rstrip().split(",")
            self.to_names.append(row[0])
            self.to_addrs.append(row[1])
            self.if_sends.append(row[2])

    def get_mail_settings(self):
        with open('mailsettings.txt') as f:
            lines = f.readlines()

        self.mailfrom = lines[0][5:].rstrip()
        self.mailcc = lines[1][3:].rstrip()
        self.mailbcc = lines[2][4:].rstrip()
        self.mailsub = lines[3][4:].rstrip()

    def get_sender_password(self):
        self.mailpass = getpass('gmailパスワードを入力してください: ')

    def get_mail_template(self):
        with open('mailbody.txt', 'r') as f:
            lines = f.readlines()[3:]

        for line in lines:
            self.mailtemplate += line

    def make_mail_body(self, to_name):
        self.mailbody = self.mailtemplate.replace("##TO_NAME##", to_name)

    def get_attachment(self):
        with open('attachment.txt', 'r') as f:
            attach = f.readlines()[4]
        self.mailattach = basename(attach)


def send_mail(
        myaddr="",
        mypass="",
        from_addr="",
        to_addrs=[],
        cc_addrs=[],
        bcc_addrs=[],
        subject="default_subject",
        mailbody="default mailbody",
        attachment="none"):

    try:
        msg = MIMEMultipart()

        # メール本体を作成する
        msg["Subject"] = subject
        msg["From"] = from_addr
        msg["To"] = ",".join(to_addrs)
        print(msg["To"])

        if cc_addrs != []:
            msg["Cc"] = ",".join(cc_addrs)
        if bcc_addrs != []:
            msg["Bcc"] = ",".join(bcc_addrs)
        msg.attach(MIMEText(mailbody))

        # ファイルを添付する
        if not(attachment == "none"):
            with open(attachment, 'rb') as f:
                attach_file = MIMEApplication(f.read(), _subtype="pdf")

            attach_file.add_header('Content-Disposition',
                                   'attachment', filename=attachment)

            msg.attach(attach_file)

        # 送信する
        smtp = smtplib.SMTP("smtp.gmail.com", 587)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(myaddr, mypass)
        smtp.send_message(msg)
        smtp.close()

        return "送信成功"

    except:
        return "送信失敗！"


def main():

    strlog = ""

    # 各種設定ファイルを読み取る
    ms = MailSettings()

    # 送付先リストごとにメールを送る
    for i, _ in enumerate(ms.to_names):

        if ms.if_sends[i] == "する":
            ms.make_mail_body(ms.to_names[i])
            ret = send_mail(
                myaddr=ms.mailfrom,
                mypass=ms.mailpass,
                from_addr=ms.mailfrom,
                to_addrs=[ms.to_addrs[i]],
                cc_addrs=[ms.mailcc],
                bcc_addrs=[ms.mailbcc],
                subject=ms.mailsub,
                mailbody=ms.mailbody,
                attachment=ms.mailattach)

        else:
            ret = "ユーザー設定により送信をスキップ"

        strlog += ms.to_names[i] + " 様: " + ret + "\n"

    # 実行ログを出力する
    with open('log.csv', 'w') as f:
        f.write(strlog)


if __name__ == '__main__':

    main()
