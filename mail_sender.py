import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mailsend(email, password):
    text = (f'Ваш логин {email},\n ваш пароль {password}')
    recipients = []
    recipients.append(email)
    server = 'smtp.mail.ru'
    user = 'placesofinterest@mail.ru'
    password = '**'


    sender = 'placesofinterest@mail.ru'
    subject = 'Места интереса МИИГАиК'


    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)


    part_text = MIMEText(text, 'plain')


    msg.attach(part_text)



    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()