import unittest
from unittest.mock import MagicMock, patch

from sens_platform.utils.administration_email import AdministrationEmail


class TestEmail(unittest.TestCase):
    def setUp(self):
        self.email = AdministrationEmail("subject", "body", "to_email@example.com")

    @patch("smtplib.SMTP")
    def test_send_email(self, mock_smtp):
        mock_smtp.return_value.sendmail.return_value = True
        self.email.send_email()
        mock_smtp.assert_called_once_with(host=self.email._host, port=self.email._port)
        mock_smtp.return_value.starttls.assert_called_once()
        mock_smtp.return_value.login.assert_called_once_with(
            self.email._from_email, password=self.email._pass
        )
        mock_smtp.return_value.sendmail.assert_called_once()
        mock_smtp.return_value.quit.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_email_exception(self, mock_smtp):
        mock_smtp.return_value.sendmail.side_effect = Exception("SMTP error")
        with self.assertRaises(Exception):
            self.email.send_email()


if __name__ == "__main__":
    unittest.main()
