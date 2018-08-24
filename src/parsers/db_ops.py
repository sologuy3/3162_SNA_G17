import pdb


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
import django
django.setup()

from data.models import Person, Email
from src.parsers.enron_parser import EnronParser


def main():
    emails = EnronParser()

    for inmem_email in emails.emails():

        if Person.objects.filter(email=inmem_email['From']).exists():
            pdb.set_trace()

        db_email = Email()
        db_email.id = inmem_email['id']
        db_email.cc = inmem_email['CC']
        db_email.bcc = inmem_email['Bcc']
        db_email.to = inmem_email['To']
        db_email.authors = inmem_email['From']

    pdb.set_trace()

if __name__ == "__main__":
    main()