import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from netbox.settings import configuration

__all_ = ("AdministrationEmail",)


class AdministrationEmail:
    _pass: str = configuration.EMAIL["PASSWORD"]
    _from_email: str = configuration.EMAIL["FROM_EMAIL"]
    _port: int = configuration.EMAIL["PORT"]
    _host: str = configuration.EMAIL["SERVER"]
    _to_email: str
    _subject: str
    _body: str

    def __init__(self, subject, body, to_email):
        self._subject = subject
        self._body = body
        self._to_email = to_email
        self._connect()

    def _connect(self):
        self.server = smtplib.SMTP(host=self._host, port=self._port)
        self.server.starttls()
        self.server.login(user=self._from_email, password=self._pass)

    def send_email(self):
        msg = MIMEMultipart()
        msg["From"] = self._from_email
        msg["To"] = self._to_email
        msg["Subject"] = self._subject
        msg.attach(MIMEText(self._body, "plain"))
        text = msg.as_string()
        self.server.sendmail(self._from_email, self._to_email, text)
        self.server.quit()
