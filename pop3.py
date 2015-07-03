#! /usr/bin/env python
# -*- coding: utf-8 -*-

import poplib
from Tkinter import *
import email
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.label_title = Label(self, text="POP3: Receive Mail", font=("Arial", 12), bg='green', width=750, height=2)
        self.label_title.pack()
        self.frm_1 = Frame(self)
        self.label_email = Label(self.frm_1, text="email:")
        self.label_email.pack(side=LEFT)
        self.entry_email = Entry(self.frm_1)
        self.entry_email.pack(side=LEFT)
        self.label_password = Label(self.frm_1, text="password:")
        self.label_password.pack(side=LEFT)
        self.entry_pwd = Entry(self.frm_1)
        self.entry_pwd.pack(side=LEFT)
        self.label_server = Label(self.frm_1, text="server:")
        self.label_server.pack(side=LEFT)
        v1 = StringVar()
        self.entry_server = Entry(self.frm_1, textvariable=v1)
        v1.set('pop3.sina.com.cn')
        self.entry_server.pack(side=LEFT)
        self.entry_pwd['show'] = '*'
        self.button_login = Button(self.frm_1, text="Login", command=self.receiveMails)
        self.button_login.pack(side=LEFT)
        self.label_mail_num = StringVar()
        self.label_state = Label(self.frm_1, textvariable=self.label_mail_num)
        self.label_state.pack(side=LEFT)
        self.label_mail_num.set("Mail number: 0 ")
        self.frm_1.pack()

    def receiveMails(self):
        str_email = self.entry_email.get()
        str_pwd = self.entry_pwd.get()
        pop3_server = self.entry_server.get()
        server = poplib.POP3(pop3_server)
        print(server.getwelcome())
        server.user(str_email)
        server.pass_(str_pwd)
        print server.stat()
        self.label_mail_num.set("Mail number: %s " % server.stat()[0])
        resp, mails, octets = server.list()
        # 可以查看返回的列表类似['1 82923', '2 2184', ...]
        print(mails)
        # 获取最新一封邮件, 注意索引号从1开始:
        index = len(mails)
        resp, lines, octets = server.retr(index)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = '\r\n'.join(lines)
        msg = Parser().parsestr(msg_content)
        self.print_info(msg)

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def guess_charset(self, msg):
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    # indent用于缩进显示:
    def print_info(self, msg, indent=0):
        if indent == 0:
            # 邮件的From, To, Subject存在于根对象上:
            for header in ['From', 'To', 'Subject']:
                value = msg.get(header, '')
                if value:
                    if header=='Subject':
                        # 需要解码Subject字符串:
                        value = self.decode_str(value)
                    else:
                        # 需要解码Email地址:
                        hdr, addr = parseaddr(value)
                        name = self.decode_str(hdr)
                        value = u'%s <%s>' % (name, addr)
                print('%s%s: %s' % ('  ' * indent, header, value))
        if (msg.is_multipart()):
            # 如果邮件对象是一个MIMEMultipart,
            # get_payload()返回list，包含所有的子对象:
            parts = msg.get_payload()
            for n, part in enumerate(parts):
                print('%spart %s' % ('  ' * indent, n))
                print('%s--------------------' % ('  ' * indent))
                # 递归打印每一个子对象:
                print_info(part, indent + 1)
        else:
            # 邮件对象不是一个MIMEMultipart,
            # 就根据content_type判断:
            content_type = msg.get_content_type()
            if content_type=='text/plain' or content_type=='text/html':
                # 纯文本或HTML内容:
                content = msg.get_payload(decode=True)
                # 要检测文本编码:
                charset = self.guess_charset(msg)
                if charset:
                    content = content.decode(charset)
                print('%sText: %s' % ('  ' * indent, content.encode('utf-8') + '...'))
            else:
                # 不是文本,作为附件处理:
                print('%sAttachment: %s' % ('  ' * indent, content_type))


if __name__ == "__main__":
    app = Application()
    app.master.title('POP3 client')
    app.master.geometry('750x450')
    app.mainloop()
