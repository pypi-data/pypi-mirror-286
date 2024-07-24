import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password,smtp_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.smtp_email    = smtp_email

    def send_email(self, to_email, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            #TTLS SECURITY
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.sendmail(self.smtp_email, to_email, msg.as_string())
            server.quit()
            print("Email sent successfully to", to_email)
        except Exception as e:
            print("Failed to send email:", e)

    def notify_agent_can_answer(self, prompt, human_agent_email,issue_id,subject=None,body=None):
        ts =  datetime.datetime.now()
        if subject==None:
            subject = f"Request for Human Agent Assistance (Issue ID: {issue_id}  && timestamp: {ts})"
        if body==None:
            body = f"Prompt from user:\n {prompt} \n\nThe AI agent has responded successfully but still requires your attention.\
                    \n timestamp: {ts} \n\n\n Best Regards, \n ZCHAR Support"
        self.send_email(human_agent_email, subject, body)

    def notify_agent_needs_help(self, prompt, human_agent_email,issue_id,subject=None,body=None):
        ts =  datetime.datetime.now()
        if subject==None:
            subject = f"Urgent Assistance Needed (Issue ID: {issue_id}  && timestamp: {ts})"
        if body==None:
            body = f"Prompt from user:\n {prompt} \n\nThe AI agent was unable to\
                      provide a response and needs your assistance.\n\n timestamp: {ts} \n\n\n Best Regards, \n ZCHAR Support"
        self.send_email(human_agent_email, subject, body)