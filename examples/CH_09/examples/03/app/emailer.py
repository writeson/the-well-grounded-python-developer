from flask import current_app
import yagmail
from threading import Thread
#from unsync import unsync


yag = yagmail.SMTP(
    user=current_app.config.get("SMTP_USERNAME"),
    password=current_app.config.get("SMTP_PASSWORD")
)


#@unsync
def send_mail(to, subject, contents):
    # yag.send(to=to, subject=subject, contents=contents)
    thr = Thread(target=yag.send, args=[to, subject, contents])
    thr.start()


