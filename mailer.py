import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import sys

gmail_user = "pythmailer@gmail.com"
gmail_pwd = "pythmailerpythmailer"
#gmail_user, gmail_pwd = "MAILADRESS@gmail.com", None


def sendAttachment(to, subject, text, attachFilename):
    """Sends a mail with an attachment, using the default user/pw
    attach is a filename string to load from, as binary data
    
    See also: send() to send regular mail without an attachment
    """
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(attachFilename, 'rb').read())
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(attachFilename))
    msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()


def send(to, subject, text):
    """Sends a mail, using the default user/pw
    
    Example: send("john.doe@gmail.com", "Hi!", "Let's get lunch today")
    
    See also: sendAttachment
    """
    msg = MIMEMultipart()
    
    msg['From'] = gmail_user
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()

    #~ mail("some.person@some.address.com",
    #~ "Hello from python!",
    #~ "This is a email sent with python",
    #~ "my_picture.jpg")
   
if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 6:
        print "Error! Usage: mailer.py to@email.com subject message"

    elif len(sys.argv) == 4:
        mail(sys.argv[1], sys.argv[2], sys.argv[3])
        
        print "Message sent to %s with sub: %s" % (sys.argv[1], sys.argv[2])
        
    elif len(sys.argv) == 5:
        mailAttach(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        
        print "Message sent to %s with sub: %s and attachment %s" %\
            (sys.argv[1], sys.argv[2], sys.argv[3])