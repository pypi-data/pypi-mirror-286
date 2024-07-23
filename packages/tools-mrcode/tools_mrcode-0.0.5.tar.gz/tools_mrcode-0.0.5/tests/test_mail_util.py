import unittest
from src.tools_mrcode import mail_util


class MailUtilTestCase(unittest.TestCase):
    def test_send(self):
        smtp_host: str = 'smtp.163.com'
        smtp_port: int = 25
        smtp_user: str = 'work_mrcode@163.com'
        smtp_pwd: str = 'NLILRISEMYIUVXPH'
        sender: str = smtp_user
        to: str = '99299684@qq.com'
        subject: str = '测试邮件'
        body: str = '<p>测试邮件内容</p><h1>测试邮件内容</h1>'
        body = (f'店铺 22 </br> '
                     f'达人获取页面可能触发了风控，请手动访问该页面，检测并解控 </br> '
                     f'当次推送成功达人数量 2 分钟 ')
        mail_util.send(smtp_host=smtp_host, smtp_port=smtp_port, smtp_user=smtp_user, smtp_pwd=smtp_pwd, sender=sender,
                       to=to,
                       subject=subject, body=body)
