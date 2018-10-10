import datetime
import json
import os
import pdb

import re

from graph_sna.parsers.enron_parser import EnronParser


def main(emails):
    mail_dir = '../maildir/'
    folders = os.listdir(path = mail_dir)
    staff_emails = set("steven.harris@enron.com") # Add the one annoying edge case by hand...

    to_regex = re.compile("From: ([a-zA-Z.]*@enron.com)")
    better_to_regex = re.compile("From: ([a-zA-Z]*.[a-zA-Z]*@enron.com)")
    for folder in folders:
        path = mail_dir + "/" + folder
        categories = os.listdir(path)
        sent_folders = [category for category in categories if "sent" in category]
        if len(sent_folders) == 0:
            continue

        # Go through sent folders / sent items and try find a source email address that matches the format
        # john.smith@enron.com (rather than abbreviated formats eg jo.th@enron.com)
        flag = False
        email_addr = ""
        for sent_folder in sent_folders:
            for file in os.listdir(path + "/" + sent_folder):
                infile = open(path + "/" + sent_folder + "/" + file).read()
                match = to_regex.search(infile)
                better_match = better_to_regex.search(infile)
                if hasattr(match, "group"):
                    if hasattr(better_match, "group"):
                        staff_emails.add(better_match.group(1))
                        print(better_match.group(1))
                        flag = True
                        break
                    else:
                        email_addr = match.group(1)
            if flag:
                break

        # Add the best available one.
        if not flag:
            staff_emails.add(email_addr)


    good_emails = []

    for i, inmem_email in enumerate(emails):

        if i % 5000 == 0:
            print(str(round(100*i/len(emails),2)) + "% done")

        inmem_email = clean(inmem_email)
        from_email = inmem_email['from']
        if from_email not in staff_emails:
            continue

        if "To" not in inmem_email:
            continue # Some emails don't have a `To` key?

        to_emails = inmem_email['To']
        valid_to_emails = [addr for addr in to_emails if addr in staff_emails and addr != '']

        if len(valid_to_emails) == 0:
            continue
        else:
            #print("{} -> {}".format(from_email, valid_to_emails))
            inmem_email['To'] = json.dumps(valid_to_emails)

        good_emails.append(inmem_email)

    print("Out of {} emails, {} were originating from and sent towards dataset staff".format(len(emails), len(good_emails)))


    with open("enrondump", "w") as out:
        out.write(json.dumps(good_emails))

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