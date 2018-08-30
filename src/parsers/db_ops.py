import json
import pdb


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()

from data.models import Person, Email
from src.parsers.enron_parser import EnronParser
import re


def main(emails):

    x_from_regex = re.compile("( *)([a-zA-Z ]*) <(.*?)>")


    for inmem_email in emails.emails():
        cleaned = clean(inmem_email)
        from_data = x_from_regex.match(cleaned['X-From'])
        from_name = from_data.group(2)
        from_email = from_data.group(3)
        if not Person.objects.filter(email=inmem_email['From']).exists():
            p = Person.objects.create(name=from_name, email=from_email)


        db_email = Email()
        db_email.id = inmem_email['id']
        db_email.cc = inmem_email['CC']
        db_email.bcc = inmem_email['Bcc']
        db_email.to = inmem_email['To']
        db_email.authors = inmem_email['From']

        if not Email.objects.filter(id=db_email.id).exists():
            email = Email.objects.create(

            )

    pdb.set_trace()

def clean(email):
    d = {}
    d['to'] = [to.replace(" ", "") for to in d['to']]
    for k, v in email:
        d[k] = v.replace("\n","")
    return d

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
    emails = get_emails_from_json()
    main(emails)