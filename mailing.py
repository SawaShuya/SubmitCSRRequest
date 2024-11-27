import smtplib
from email.mime.text import MIMEText

import ssm_client

from_address = "no-reply@devdevnetwork.com"
charset = "UTF-8"
smtp_endpoint= "email-smtp.ap-northeast-1.amazonaws.com"

smtp_user = ssm_client.get_params('/lambda/SubmitCSRRequest/SMTP_USER')
smtp_user_password = ssm_client.get_params('/lambda/SubmitCSRRequest/SMTP_USER_PASSWORD')

def send(id, to_address):
    print(f"Send Mail to {to_address}")
    subject = "CSR Submitted Sccessfully"
    body = f"Your application was successful and your ID is  {id}. \nPlease wait a moment for completion."
    smtpobj = smtplib.SMTP(smtp_endpoint, 587)
    smtpobj.ehlo() 
    smtpobj.starttls()
    smtpobj.login(smtp_user, smtp_user_password)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject

    smtpobj.sendmail(from_address, to_address, msg.as_string())

    smtpobj.quit()