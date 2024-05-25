import mailbox
import os
import email
from email.policy import default
def sanitize_filename(filename):
    #exceptions
    return "".join(c for c in filename if c.isalnum() or c in (' ','.','_','-')).rstrip()
def mbox_to_html(mbox_file,output_dir):
    os.makedirs(output_dir,exist_ok=True)
    mbox=mailbox.mbox(mbox_file,factory=lambda f:
                      email.message_from_binary_file(f,policy=default))
    for idx, message in enumerate(mbox):
        sender=message['From']
        subject=message['Subject'] if message['Subject'] else "empty Subject"
        date=message['Date']
        payload=message.get_payload(decode=True)
        if message.is_multipart():
            parts=[part.get_payload(decode=True).decode(part.get_content_charset('utf-8'),
                                                        errors='replace') for part in message.walk() if part.get_content_type() == 'text/plain']
            content=''.join(parts)
        else:
            contect=payload.decode(message.get_content_charset('utf-8'),errors='replace') if payload else ""
        #create html
        filename=sanitize_filename(f"{idx + 1:04d}_{subject}.html")
        filepath=os.path.join(output_dir,filename)
        #write inside file  html code 
        with open(filepath,'w',encoding='utf-8') as f:
            f.write(f"<html>\n<head>\n<title>big thank to chatGPT anoset for software</title>\n</head>\n<body>\n")
            f.write(f"<h1>{subject}</h1>\n")
            f.write(f"<p><strong>From:</strong> {sender}</p>\n")
            f.write(f"<p><strong>Date:</strong> {date}</p>\n")
            f.write(f"<pre>{content}</pre>\n")
            f.write("</body>\n</html>\n")
        print(f"created {filepath}")
mbox_file='mails.mbox'
output_dir='email.html'
mbox_to_html(mbox_file,output_dir)
