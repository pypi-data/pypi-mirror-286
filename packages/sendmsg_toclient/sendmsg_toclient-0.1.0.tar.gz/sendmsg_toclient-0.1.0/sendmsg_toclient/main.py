from smtplib import SMTP


class SendEmail():
    def __init__(self, email: str, password: str, ip_adress='smtp.gmail.com', port=587):
        self.email = email
        self.password = password
        self.server = SMTP(ip_adress, port)
        self.server.starttls()

    def login(self):
        self.server.login(self.email, self.password)

    def send(self, to, subject, body):
        self.login()
        message = f'Subject: {subject}\n\n{body}'
        self.server.sendmail(self.email, to, message)
        self.server.quit()
