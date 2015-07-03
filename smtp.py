#! /usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import parseaddr, formataddr
import smtplib
import tkMessageBox
import tkFileDialog
import os


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(
            self, text='SMTP: Send Email', bg="green", font=("Arial", 12), width=600, height=2)
        self.helloLabel.pack()
        # From:###### Password:######
        self.frm = Frame(self)
        self.frm0 = Frame(self.frm)
        self.frm_11 = Frame(self.frm0)
        self.Label_From11 = Label(self.frm_11, text="   From:")
        self.Label_From11.pack(side=LEFT)
        self.From = Entry(self.frm_11)
        self.From.pack(side=LEFT)
        self.frm_11.grid(row=0, column=0)
        self.frm_12 = Frame(self.frm0)
        self.Label_Pwd12 = Label(self.frm_12, text="Password:")
        self.Label_Pwd12.pack(side=LEFT)
        self.Password = Entry(self.frm_12)
        self.Password.pack(side=LEFT)
        self.Password['show'] = '*'
        self.frm_12.grid(row=0, column=1)
        self.frm0.grid(row=0, column=0)
        # To:######
        self.frm_2 = Frame(self.frm)
        self.Label_To = Label(self.frm_2, text="       To:")
        self.Label_To.pack(side=LEFT)
        self.To = Entry(self.frm_2)
        self.To.pack(side=LEFT)
        self.Label_Server = Label(self.frm_2, text="SMTP Server:")
        self.Label_Server.pack(side=LEFT)
        v1 = StringVar()
        self.Server = Entry(self.frm_2, textvariable=v1)
        v1.set('smtp.sina.com.cn')
        self.Server.pack(side=LEFT)
        self.frm_2.grid(row=1, column=0)
        # Subject
        self.frm_3 = Frame(self.frm)
        self.Label_Subject = Label(self.frm_3, text="Subject:")
        self.Label_Subject.pack(side=LEFT)
        self.Subject = Entry(self.frm_3)
        self.Subject.pack(side=LEFT)
        self.frm_3.grid(row=2, column=0)
        # Text
        self.frm_4 = Frame(self.frm)
        self.Label_Text = Label(self.frm_4, text="Text:")
        self.Label_Text.pack()
        self.text_msg = Text(self.frm_4, width=80, height=18)
        self.text_msg.pack()
        self.frm_4.grid(row=3, column=0)
        self.frm.pack()
        # open
        self.frm_5 = Frame(self.frm)
        self.file_entry = Entry(self.frm_5)
        self.file_entry.pack(side=LEFT)
        self.Button_Open = Button(self.frm_5, text="Open", command=self.Open)
        self.Button_Open.pack(side=LEFT)
        self.frm_5.grid(row=4, column=0)
        # Button send
        self.Button_Send = Button(self, text="Send", command=self.Send)
        self.Button_Send.pack(side=BOTTOM)

    def _format_addr(self, s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def Send(self):
        str_From = self.From.get()
        str_Password = self.Password.get()
        str_To = self.To.get()
        str_Subject = self.Subject.get()
        str_Server = self.Server.get()
        str_Text = self.text_msg.get('0.0', END)
        smtp_server = str_Server
        server = smtplib.SMTP(smtp_server, 25)
        msg = MIMEMultipart()
        msg['From'] = self._format_addr(u'Python爱好者 <%s>' % str_From)
        msg['To'] = self._format_addr(u'Python好友 <%s>' % str_To)
        msg['Subject'] = Header(str_Subject, 'utf-8').encode()
        msg.attach(MIMEText(str_Text, 'plain', 'utf-8'))
        str_file = self.file_entry.get()
        if str_file is "" or str_file is None:
            server.login(str_From, str_Password)
            server.sendmail(str_From, [str_To], msg.as_string())
            server.quit()
            tkMessageBox.showinfo('Message', '邮件发送成功~')
        else:
            print str_file
            ff = open(str_file, 'rb')
            ff.close()
            print os.path.basename(str_file)
            print os.path.basename(str_file).split('.')[-1]
            # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
            with open(str_file, 'rb') as f:
                # 设置附件的MIME的类型，文件后缀和文件名:
                mime = MIMEBase('application', os.path.basename(str_file).split('.')[-1], filename=os.path.basename(str_file))
                # 加上必要的头信息:
                att_header = Header(os.path.basename(str_file), 'utf-8')
                mime.add_header(
                    'Content-Disposition', 'attachment; filename="%s"' % att_header)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)
            server.login(str_From, str_Password)
            server.sendmail(str_From, [str_To], msg.as_string())
            server.quit()
            tkMessageBox.showinfo('Message', '邮件发送成功~')

    def Open(self):
        self.file_entry.delete(0, END)
        # 清空entry里面的内容
        # 调用filedialog模块的askdirectory()函数去打开文件夹
        filepath = tkFileDialog.askopenfilename()
        if filepath:
            self.file_entry.insert(0, filepath)
            # 将选择好的路径加入到entry里面


if __name__ == '__main__':
    app = Application()
    app.master.title('SMTP Client')
    app.master.geometry('600x450')
    app.mainloop()
