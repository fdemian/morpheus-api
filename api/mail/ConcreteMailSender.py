import smtplib


class ConcreteMailSender:

    def __init__(self, host, port):
        self.mailer = smtplib.SMTP(host, port=port)

    def send(self, sender, recipient, message):
        self.mailer.sendmail(sender, recipient, message)
        self.mailer.quit()
