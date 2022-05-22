import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_password_reset_email(
    email_receiver,
    reset_link,
    mailSender=os.environ["MAIL_ADDRESS"],
    mailPwd=os.environ["MAIL_PASSWORD"],
):
    smtpHost = "smtp.gmail.com"
    smtpPort = 587
    mailSubject = "Reset Password"
    mailContentHtml = f"Reset Link: <br/> <a href='{reset_link}'> Click here to create new password</a>"

    # create message object
    msg = MIMEMultipart()
    msg["From"] = mailSender
    msg["To"] = email_receiver
    msg["Subject"] = mailSubject
    msg.attach(MIMEText(mailContentHtml, "html"))

    # Send message object as email using smptplib
    s = smtplib.SMTP(smtpHost, smtpPort)
    s.starttls()
    s.login(mailSender, mailPwd)
    msgText = msg.as_string()
    sendErrs = s.sendmail(mailSender, [email_receiver], msgText)
    s.quit()

    # check if errors occured and handle them accordingly
    if not len(sendErrs.keys()) == 0:
        raise Exception("Errors occurred while sending email", sendErrs)


if __name__ == "__main__":

    recipient = os.environ["TEST_RECIPIENT"]
    send_password_reset_email(recipient)
    print("execution complete...")
