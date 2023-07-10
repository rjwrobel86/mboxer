#Converts a GMail 'mbox' export into a folder of emails in txt format 
import os
import re
import pandas as pd
import string
import mailbox
from email import message_from_string

def extract_text_from_email_message(message):
    if message.is_multipart():
        text_parts = []
        for part in message.walk():
            content_type = part.get_content_type()
            if content_type == 'text/plain':
                text_parts.append(part.get_payload(decode=True).decode())
        return '\n'.join(text_parts)
    else:
        return message.get_payload(decode=True).decode()

def convert_mbox_to_emails(mbox_file, output_folder):
    mbox = mailbox.mbox(mbox_file)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, message in enumerate(mbox):
        labels = message.get('X-Gmail-Labels', '')
        if 'Lead' in labels:
            subject = message['subject']
            email_file = os.path.join(output_folder, f"{i+1:04d}_{subject}.txt")

            text_content = extract_text_from_email_message(message)
            with open(email_file, 'w') as f:
                f.write(text_content)

    mbox.close()

output_folder = '/Users/robertwrobel/Code/mboxer/output'

convert_mbox_to_emails("mail.mbox", output_folder)