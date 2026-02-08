import smtplib
from email.mime.text import MIMEText
import os

class NotificationService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_pass = os.getenv("EMAIL_PASS")

    def send_email_alert(self, to_email, region, risk_level):
        """
        Sends an email alert.
        """
        subject = f"URGENT: Landslide Risk Alert for {region}"
        body = f"A {risk_level} risk of landslide has been detected in {region}. Please take necessary precautions."
        
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = to_email

        try:
            if not self.email_user or not self.email_pass:
                print("Email credentials not set. Skipping email alert.")
                return

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            server.sendmail(self.email_user, to_email, msg.as_string())
            server.quit()
            print(f"Email sent to {to_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")

    def send_sms_alert(self, phone_number, region, risk_level):
        """
        Placeholder for SMS alert (e.g., using Twilio).
        """
        print(f"SMS Alert to {phone_number}: High Risk in {region}!")

if __name__ == "__main__":
    service = NotificationService()
    service.send_email_alert("admin@example.com", "Kerala_Idukki", "High")
