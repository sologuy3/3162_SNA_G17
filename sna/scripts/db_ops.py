import datetime
import json
import os
import pdb

from graph_sna.models import Person, Email
from graph_sna.parsers.enron_parser import EnronParser
import re
import traceback

def main(emails):


    for i, inmem_email in enumerate(emails):
        print(str(round(100*i/len(emails),2)) + "% done")
        inmem_email = clean(inmem_email)

        if "To" not in inmem_email:
            continue # Some emails don't have a to key?
        from_email = inmem_email['from']

        # Don't include emails if they don't originate from graph_sna
        if "@enron" not in from_email:
            continue

        person, created = Person.objects.get_or_create(email_address=from_email)

        db_email = Email()
        db_email.id = inmem_email['id']
        db_email.cc = inmem_email['X-cc']
        db_email.bcc = inmem_email['X-bcc']
        db_email.to = inmem_email['To']
        db_email.subject = inmem_email['Subject']

        datestring = inmem_email['datetime'].split(" (")[0]
        db_email.time_sent = datetime.datetime.strptime(datestring, "%a, %d %b %Y %H:%M:%S %z")

        email, created = Email.objects.get_or_create(id=db_email.id,time_sent=db_email.time_sent, author=person)

        if created:
            if inmem_email['datetime'][6] == " ":  # Check if DOM < 10 by seeing if 7th character is a space
                inmem_email['datetime'] = inmem_email['datetime'].replace(", ", ", 0")  # Make day-of-month 0 padded
            inmem_email['datetime'] = inmem_email['datetime'].split(" (")[0]
            email.author = person
        try:
            recipient, created = Person.objects.get_or_create(email=db_email.to[0])
            author, created = Person.objects.get_or_create(email=from_email)
            email.recipients.add(recipient)
            email.author = author
        except Exception as e:
            traceback.print_exc()
            pdb.set_trace()

        email.save()


def clean(email):
    d = {}

    if 'To' in email:
        d['To'] = [to.replace(" ", "") for to in email['To']]

    for k, v in email.items():
        if k == "To":
            continue
        try:
            if isinstance(v, list):
                d[k] = v[0].replace("\n","") # 0th index for first subject line?
            else:
                d[k] = v.replace("\n", "")
        except Exception as e:
            print(e)

    return d


def get_emails_from_json():

    json_data = ""
    with open("graph_sna/parsers/data.json") as read:
        json_data = read.read()

    return json.loads(json_data)


def save_json():
    emails = EnronParser()

    print("Json is outputting")
    json = emails.get_email_json()

    with open("data.json", "w") as out:
        out.write(json)

    return emails.emails

def run():

    load = True

    if load:
        emails = get_emails_from_json()
    else:
        emails = save_json()

    main(emails)