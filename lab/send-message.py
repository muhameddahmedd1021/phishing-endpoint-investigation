"""Send one sample email to the local SMTP capture service."""
import argparse,smtplib,email.utils,datetime
from email.message import EmailMessage
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--recipient',default='mohamedahmed@company.example');p.add_argument('--url',default='http://10.0.2.2:8766/phishing/Benefits-Review.zip');a=p.parse_args()
m=EmailMessage();m['From']='Employee Benefits <benefits@people-update.example>';m['Reply-To']='support@benefits-review.example';m['To']=a.recipient;m['Subject']='Action required: benefits review';m['Date']=email.utils.format_datetime(datetime.datetime.now(datetime.timezone.utc));m['Message-ID']=email.utils.make_msgid(domain='people-update.example')
m.set_content('Please review the benefits document before the end of the day.\nDownload: '+a.url+'\nThe same archive is attached.\n')
m.add_attachment(Path(a.archive).read_bytes(),maintype='application',subtype='zip',filename='Benefits-Review.zip')
with smtplib.SMTP('127.0.0.1',2525) as c:c.send_message(m)
print(m['Message-ID'])
