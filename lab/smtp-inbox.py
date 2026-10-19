"""Local SMTP capture service for the isolated email lab."""
import argparse,asyncio,email,json,hashlib,datetime
from email import policy
from pathlib import Path
from aiosmtpd.controller import Controller

class Inbox:
 def __init__(self,output):self.output=Path(output);self.output.mkdir(parents=True,exist_ok=True)
 async def handle_DATA(self,server,session,envelope):
  message=email.message_from_bytes(envelope.original_content,policy=policy.default)
  name='message-%03d.eml'%(len(list(self.output.glob('*.eml')))+1)
  (self.output/name).write_bytes(envelope.original_content)
  attachments=list(message.iter_attachments())
  row={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'mail_from':envelope.mail_from,'recipients':envelope.rcpt_tos,'message_id':str(message['Message-ID']),'subject':str(message['Subject']),'file':name,'attachment_sha256':hashlib.sha256(attachments[0].get_payload(decode=True)).hexdigest() if attachments else None}
  with (self.output/'delivery.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  return '250 Message accepted'

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',default='mail');p.add_argument('--port',type=int,default=2525);a=p.parse_args()
 c=Controller(Inbox(a.output),hostname='127.0.0.1',port=a.port);c.start()
 try:asyncio.run(asyncio.Event().wait())
 except KeyboardInterrupt:pass
 finally:c.stop()
