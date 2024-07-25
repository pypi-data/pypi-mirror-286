
# 异步调用支持
import asyncio
# 网络延迟测试
import ping3
# gmail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.base import MIMEBase
from email import encoders


# 发件人和收件人信息
sender_email = "774190438@qq.com"
receiver_email = "774190438@qq.com"
password = "jocbkltbzmysbfgf"
smtp_server = "smtp.qq.com"  # QQ邮箱的SMTP服务器地址
smtp_port = 587  # QQ邮箱的SMTP服务器端口（通常为587）


async def SendMail(self,*text: any)->None:
    try:
        """发送提醒消息"""
        # 登录QQ邮箱
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # 启用TLS加密
        server.login(sender_email, password)


        # 发送邮件

        #subject = "策略提醒 ag2408 %d" % price
        subject = str(text)
        contents = str(text)
        #subject = "策略提醒"
        #contents = "策略提醒"

        msg = MIMEText(contents, 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = formataddr(["BLEngine量化管家", sender_email])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["二寸丹心", receiver_email])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = subject  # 邮件的主题，也可以说是标题
        # yag.send(receiver_email, subject, contents)
        server.sendmail(sender_email, receiver_email, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        
        server.quit()  # 关闭连接
        #self.output("邮件已发送成功！")
        print("邮件已发送成功！")


    except smtplib.SMTPServerDisconnected:
        #self.output("SMTP服务器连接中断")
        print("SMTP服务器连接中断")
        #server.quit()  # 关闭连接
        # 登录QQ邮箱
        #server = smtplib.SMTP(smtp_server, smtp_port)
        #server.starttls()  # 启用TLS加密
        #server.login(sender_email, password)
        #self.output("邮箱已登录")
    #except smtplib.SMTPAuthenticationError:
        #self.output("登录认证失败")
        
    #except Exception as e:
        #self.output(f"发送邮件时发生错误: {e}")


def NetDelay(self)->int:
    delay=ping3.ping("www.baidu.com")
    if delay is not None:
        ret=delay
    else:
        ret=999
    return ret