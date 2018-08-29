import json
import pdb


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()

from data.models import Person, Email
from src.parsers.enron_parser import EnronParser


def main():


    for inmem_email in emails.emails():

        if Person.objects.filter(email=inmem_email['From']).exists():
            pass

        db_email = Email()
        db_email.id = inmem_email['id']
        db_email.cc = inmem_email['CC']
        db_email.bcc = inmem_email['Bcc']
        db_email.to = inmem_email['To']
        db_email.authors = inmem_email['From']

    pdb.set_trace()

def get_emails_from_json():

    json_data = ""
    with open("data.json") as read:
        json_data = read.read()

    return json.loads(json_data)


def save_json():
    emails = EnronParser()
    print("Json is outputting")
    json = emails.get_email_json()

    with open("data.json", "w") as out:
        out.write(json)

if __name__ == "__main__":
    d = get_emails_from_json()

    pdb.set_trace()